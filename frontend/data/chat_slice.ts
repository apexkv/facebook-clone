import { UserType } from '@/types/types';
import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export type MessageType = {
    user: UserType;
    message: string;
    time: string;
    read: boolean;
    direction: "received" | "sent";
}

export type ChatUserType = {
    id: string;
    friend: UserType;
}

export type ChatType = {
    user: ChatUserType;
    new_messages: number;
    messages: MessageType[];
    is_opened: boolean;
}

export type ChatListType = {
    users: ChatUserType[];
	chats: ChatType[];
    minimized_chats: ChatType[];
    active_chats: ChatType[];
};

export type EventType = {
    type: "friend.online" | "friend.offline" | "friend.typing.start" | "friend.typing.stop";
    data: any
}

const initialState: ChatListType = {
    chats: [],
    minimized_chats: [],
    active_chats: [],
    users: [],
};

export const chatSlice = createSlice({
	name: 'chat',
	initialState,
	reducers: {
        createNewChat: (state, action: PayloadAction<ChatType>) => {
            const new_chat = action.payload;
            if(state.active_chats.some((chat) => chat.user.id === new_chat.user.id)){
                state.active_chats = state.active_chats.map((chat) => {
                    if (chat.user.id === new_chat.user.id) {
                        return {
                            ...chat,
                            is_opened: true,
                        };
                    }
                    return chat;
                });
            }else{
                const current_chat = state.chats.find((chat) => chat.user.id === new_chat.user.id);
                if(current_chat){
                    state.active_chats = [current_chat, ...state.active_chats];
                }else{
                    state.active_chats = [new_chat, ...state.active_chats];
                }
                state.minimized_chats = state.minimized_chats.filter((chat) => chat.user.id !== new_chat.user.id);
            }
            if(state.active_chats.length > 3) {
                const minimized_chat = state.active_chats.pop();
                if(minimized_chat) {
                    if(state.minimized_chats.some((chat) => chat.user.id === minimized_chat.user.id)) return;
                    state.minimized_chats = [minimized_chat, ...state.minimized_chats];
                }
            }
            if(state.minimized_chats.length > 3) {
                state.minimized_chats.pop();
            }
            if(state.chats.some((chat) => chat.user.id === new_chat.user.id)) return;
            state.chats = [new_chat, ...state.chats]; 
        },
        closeActiveChat: (state, action: PayloadAction<ChatUserType>) => {
            state.active_chats = state.active_chats.filter((chat) => chat.user.id !== action.payload.id);
        },
        closeMinimizedChat: (state, action: PayloadAction<ChatUserType>) => {
            state.minimized_chats = state.minimized_chats.filter((chat) => chat.user.id !== action.payload.id);
        },
        addNewUser: (state, action: PayloadAction<ChatUserType>) => {
            if(state.users.some((user) => user.id === action.payload.id)) return;
            state.users = [action.payload, ...state.users];
        },
        removeUser: (state, action: PayloadAction<ChatUserType>) => {
            state.users = state.users.filter((user) => user.id !== action.payload.id);
        },
        addMessage: (state, action: PayloadAction<{ user: ChatUserType, message: MessageType }>) => {
            state.chats = state.chats.map((chat) => {
                if (chat.user.id === action.payload.user.id) {
                    return {
                        ...chat,
                        messages: [...chat.messages, action.payload.message],
                    };
                }
                return chat;
            });
            state.active_chats = state.active_chats.map((chat) => {
                if (chat.user.id === action.payload.user.id) {
                    return {
                        ...chat,
                        messages: [...chat.messages, action.payload.message],
                    };
                }
                return chat;
            });
            state.minimized_chats = state.minimized_chats.map((chat) => {
                if (chat.user.id === action.payload.user.id) {
                    return {
                        ...chat,
                        messages: [...chat.messages, action.payload.message],
                        new_messages: chat.new_messages + 1,
                    };
                }
                return chat;
            });
        },
        minimizeActiveChat: (state, action: PayloadAction<ChatUserType>) => {
            const chat = state.active_chats.find((chat) => chat.user.id === action.payload.id);
            if(!chat) return;
            state.active_chats = state.active_chats.filter((chat) => chat.user.id !== action.payload.id);
            state.minimized_chats = [chat, ...state.minimized_chats];
        },
        openMinimizedChat: (state, action: PayloadAction<ChatUserType>) => {
            const chat = state.minimized_chats.find((chat) => chat.user.id === action.payload.id);
            if(!chat) return;
            state.minimized_chats = state.minimized_chats.filter((chat) => chat.user.id !== action.payload.id);
            state.active_chats = [{...chat, is_opened:true}, ...state.active_chats];
            if(state.active_chats.length > 3) {
                const minimized_chat = state.active_chats.pop();
                if(minimized_chat) {
                    if(state.minimized_chats.some((chat) => chat.user.id === minimized_chat.user.id)) return;
                    state.minimized_chats = [minimized_chat, ...state.minimized_chats];
                }
            }
        },
        toggleActiveChat: (state, action: PayloadAction<ChatUserType>) => {
            state.active_chats = state.active_chats.map((chat) => {
                if (chat.user.id === action.payload.id) {
                    return {
                        ...chat,
                        is_opened: !chat.is_opened,
                    };
                }
                return chat;
            })
        },
        changeUserStatusOrAddUser: (state, action: PayloadAction<ChatUserType>) => {
            const user = action.payload;
            const is_user_in_users = state.users.filter((u) => u.id === user.id);

            if(is_user_in_users.length > 0){
                state.users = state.users.filter((u) => u.id !== user.id);
            }
            if(user.friend.is_online){
                state.users.unshift(user);
            }
            else{
                state.users.push(user);
            }
        }            
	},
});

export const { addMessage, addNewUser, closeActiveChat, closeMinimizedChat, createNewChat, minimizeActiveChat, openMinimizedChat, removeUser, toggleActiveChat, changeUserStatusOrAddUser } = chatSlice.actions;
export default chatSlice.reducer;