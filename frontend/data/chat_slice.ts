import { UserType } from '@/types/types';
import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export type MessageType = {
    id: string;
    user: UserType;
    content: string;
    created_at: string;
    is_read: boolean;
    direction: "received" | "sent";
    room: string;
}

export type ChatUserType = {
    id: string;
    friend: UserType;
    last_message_at: string;
    unread_count: number;
    is_active: boolean;
    last_message: string | null;
    typing: boolean;
    messages: MessageType[];
    msg_read?: boolean;
}

export type EventType = {
    type: "friend.online" | "friend.offline" | "friend.typing.start" | "friend.typing.stop" | "chat.message";
    data: any
}

export type ChatListType = {
    chat_users: ChatUserType[];
	online_users: ChatUserType[];
    msg_notifications: MessageType[];
    unread_count: number;
};

const initialState: ChatListType = {
    chat_users: [],
    online_users: [],
    msg_notifications: [],
    unread_count: 0
};

export const chatSlice = createSlice({
	name: 'chat',
	initialState,
	reducers: {
        updateIsActive: (state, action: PayloadAction<string>) => {
            const pathname = action.payload;
            state.chat_users = state.chat_users.map((user) => {
                if (user.id === pathname.split("/")[2]) {
                    return { ...user, is_active: true };
                }
                return { ...user, is_active: false };
            })
            state.online_users = state.online_users.map((user) => {
                if (user.id === pathname.split("/")[2]) {
                    return { ...user, is_active: true };
                }
                return { ...user, is_active: false };
            })
        },
        addChatUserList: (state, action: PayloadAction<ChatUserType[]>) => {
            const users = action.payload;
            users.forEach((user) => {
                const index = state.chat_users.findIndex((u) => u.id === user.id);
                const indexOnline = state.online_users.findIndex((u) => u.id === user.id && u.friend.is_online);
                if (index === -1) {
                    state.chat_users.push(user);
                } else {
                    state.chat_users[index] = user;
                }
                if (indexOnline === -1 && user.friend.is_online) {
                    state.online_users.push(user);
                }
            });
        },
        addChatOnlineUserList: (state, action: PayloadAction<ChatUserType[]>) => {
            const users = action.payload;
            users.forEach((user) => {
                const index = state.online_users.findIndex((u) => u.id === user.id);
                if (index === -1) {
                    state.online_users.push(user);
                } else {
                    state.online_users[index] = user;
                }
            });
        },
        addChatUser: (state, action: PayloadAction<ChatUserType>) => {
            const new_user = {...action.payload, typing: false}
            const user_exist = state.chat_users.filter((user)=>user.id === new_user.id)
            const online_user_exist = state.online_users.filter((user)=>user.id === new_user.id)
            if(user_exist.length === 0 && online_user_exist.length === 0){
                const index = state.chat_users.findIndex((user) => user.last_message_at < new_user.last_message_at);
                if(index === -1){
                    state.chat_users.unshift(new_user);
                }else{
                    state.chat_users.splice(index, 0, new_user);
                }
            }
        },
        addChatOnlineUser: (state, action: PayloadAction<ChatUserType>) => {
            const new_user = {...action.payload, typing: false, messages: [] }
            const user_exist = state.online_users.filter((user)=>user.id === new_user.id)
            if(user_exist.length === 0){
                state.online_users.unshift(new_user);
            }
            if(user_exist.length > 0){
                if(!new_user.friend.is_online){
                    state.online_users = state.online_users.filter((user)=>user.id !== new_user.id)
                }
            }
            state.chat_users = state.chat_users.map((user)=>{
                if(user.id === new_user.id){
                    return new_user
                }
                return user
            })
        },
        removeChatOnlineUser: (state, action: PayloadAction<ChatUserType>) => {
            const user = action.payload;
            state.online_users = state.online_users.filter((u) => u.id !== user.id);
        },
        updateChatPosition: (state, action: PayloadAction<ChatUserType>) => {
            const data = action.payload;
            const index = state.chat_users.findIndex((u) => u.id === data.id);
            if (index !== -1) {
                state.chat_users.splice(index, 1);
            }
            state.chat_users.unshift(data);         
        },
        markMessagesRead: (state, action: PayloadAction<string>) => {
            const room = action.payload;
            state.chat_users = state.chat_users.map((user) => {
                if (user.id === room) {
                    return { ...user, unread_count: 0 };
                }
                return user;
            });
            state.online_users = state.online_users.map((user) => {
                if (user.id === room) {
                    return { ...user, unread_count: 0 };
                }
                return user;
            });
        },
        roomStartTyping: (state, action: PayloadAction<string>) => {
            const room = action.payload;
            state.chat_users = state.chat_users.map((user) => {
                if (user.id === room) {
                    return { ...user, typing: true };
                }
                return user;
            });
            state.online_users = state.online_users.map((user) => {
                if (user.id === room) {
                    return { ...user, typing: true };
                }
                return user;
            });
        },
        roomStopTyping: (state, action: PayloadAction<string>) => {
            const room = action.payload;
            state.chat_users = state.chat_users.map((user) => {
                if (user.id === room) {
                    return { ...user, typing: false };
                }
                return user;
            });
            state.online_users = state.online_users.map((user) => {
                if (user.id === room) {
                    return { ...user, typing: false };
                }
                return user;
            });
            
        },
        newMessage: (state, action: PayloadAction<MessageType>) => {
            const message = action.payload
            state.chat_users = state.chat_users.map((user) => {
                if (user.id === message.room) {
                    return { 
                        ...user, 
                        last_message: message.content, 
                        last_message_at: message.created_at, 
                        unread_count: user.unread_count + 1,
                        messages: [...user.messages, message]
                    };
                }
                return user;
            });
            state.online_users = state.online_users.map((user) => {
                if (user.id === message.room) {
                    return { 
                        ...user, 
                        last_message: message.content, 
                        last_message_at: message.created_at, 
                        unread_count: user.unread_count + 1,
                        messages: [...user.messages, message]
                    };
                }
                return user;
            });
            const room_index = state.chat_users.findIndex((user) => user.id === message.room);
            
            if(room_index === -1){
                state.chat_users.unshift({
                    id: message.room,
                    friend: message.user,
                    last_message_at: message.created_at,
                    unread_count: 1,
                    is_active: false,
                    last_message: message.content,
                    typing: false,
                    messages: [message]
                })
            }
            if(room_index > 0){
                const room = state.chat_users[room_index];
                state.chat_users.splice(room_index, 1);
                state.chat_users.unshift(room);
            }
            const msg_in_notification = state.msg_notifications.filter((msg)=>msg.id === message.id)
            if(msg_in_notification.length === 0){
                state.msg_notifications.unshift(message)
            }
            if(state.msg_notifications.length > 5){
                state.msg_notifications.pop()
            }
            
        },
        readAllMessages: (state, action: PayloadAction<string>) => {
            const room = action.payload;
            state.chat_users = state.chat_users.map((user) => {
                if (user.id === room) {
                    return { 
                        ...user,
                        msg_read: true,
                    };
                }
                return user;
            });            
            state.online_users = state.online_users.map((user) => {
                if (user.id === room) {
                    return { 
                        ...user,
                        msg_read: true,
                    };
                }
                return user;
            });
        },
        emptyRoomMessages: (state, action: PayloadAction<string>) => {
            const room = action.payload;
            state.chat_users = state.chat_users.map((user) => {
                if (user.id === room) {
                    return { 
                        ...user, 
                        messages: [],
                        unread_count: 0
                    };
                }
                return user;
            });
            state.online_users = state.online_users.map((user) => {
                if (user.id === room) {
                    return { 
                        ...user, 
                        messages: [],
                        unread_count: 0
                    };
                }
                return user;
            });
        },
        resetMsgRead: (state, action: PayloadAction<string>) => {
            const room = action.payload;
            state.chat_users = state.chat_users.map((user) => {
                if (user.id === room) {
                    return { 
                        ...user,
                        msg_read: false,
                    };
                }
                return user;
            });            
            state.online_users = state.online_users.map((user) => {
                if (user.id === room) {
                    return { 
                        ...user,
                        msg_read: false,
                    };
                }
                return user;
            });
        },
        closeNotification: (state, action: PayloadAction<string>) => {
            const id = action.payload;
            state.msg_notifications = state.msg_notifications.filter((msg) => msg.id !== id);
        },
        emptyNotifications: (state) => {
            state.msg_notifications = [];
        }
        
	},
});

export const { 
    updateIsActive, 
    addChatUserList, 
    addChatUser, 
    addChatOnlineUser, 
    addChatOnlineUserList, 
    removeChatOnlineUser, 
    updateChatPosition,
    markMessagesRead,
    roomStartTyping,
    roomStopTyping,
    newMessage,
    readAllMessages,
    emptyRoomMessages,
    resetMsgRead,
    closeNotification,
    emptyNotifications
} = chatSlice.actions;
export default chatSlice.reducer;