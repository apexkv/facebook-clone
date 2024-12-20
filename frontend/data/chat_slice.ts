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

export type ChatType = {
    user: UserType;
    new_messages: number;
    messages: MessageType[];
    is_opened: boolean;
}

export type ChatListType = {
    users: UserType[];
	chats: ChatType[];
    minimized_chats: ChatType[];
    active_chats: ChatType[];
};

const initialState: ChatListType = {
    chats: [],
    minimized_chats: [],
    active_chats: [],
    users: [
        {
            id: "sdfs1",
            full_name: "John Doe",
            created_at: "2021-10-10",
            is_friend: true,
            is_online: true,
            mutual_friends: 10,
            mutual_friends_list: [],
            mutual_friends_name_list: [],
            received_request: false,
            sent_request: false,
            req_id: "sdfssd",
        },
        {
            id: "sdfs2",
            full_name: "Clair Doe",
            created_at: "2021-10-10",
            is_friend: true,
            is_online: true,
            mutual_friends: 10,
            mutual_friends_list: [],
            mutual_friends_name_list: [],
            received_request: false,
            sent_request: false,
            req_id: "sdfssd",
        },
        {
            id: "sdfs3",
            full_name: "Ben Doe",
            created_at: "2021-10-10",
            is_friend: true,
            is_online: true,
            mutual_friends: 10,
            mutual_friends_list: [],
            mutual_friends_name_list: [],
            received_request: false,
            sent_request: false,
            req_id: "sdfssd",
        },
        {
            id: "sdfs4",
            full_name: "Alex Dumpy",
            created_at: "2021-10-10",
            is_friend: true,
            is_online: true,
            mutual_friends: 10,
            mutual_friends_list: [],
            mutual_friends_name_list: [],
            received_request: false,
            sent_request: false,
            req_id: "sdfssd",
        },
        {
            id: "sdfs5",
            full_name: "Penny Doe",
            created_at: "2021-10-10",
            is_friend: true,
            is_online: true,
            mutual_friends: 10,
            mutual_friends_list: [],
            mutual_friends_name_list: [],
            received_request: false,
            sent_request: false,
            req_id: "sdfssd",
        },
        {
            id: "sdfs6",
            full_name: "Hailey Dumpy",
            created_at: "2021-10-10",
            is_friend: true,
            is_online: true,
            mutual_friends: 10,
            mutual_friends_list: [],
            mutual_friends_name_list: [],
            received_request: false,
            sent_request: false,
            req_id: "sdfssd",
        },
        {
            id: "sdfs7",
            full_name: "Nikki Doe",
            created_at: "2021-10-10",
            is_friend: true,
            is_online: true,
            mutual_friends: 10,
            mutual_friends_list: [],
            mutual_friends_name_list: [],
            received_request: false,
            sent_request: false,
            req_id: "sdfssd",
        },
    ],
};

export const chatSlice = createSlice({
	name: 'chat',
	initialState,
	reducers: {
        createNewChat: (state, action: PayloadAction<ChatType>) => {
            /*
            add new chat to active chats and chats. when creating new chat, 
            check if chat already exists and also only can have 3 active chats other 
            chats will be minimized. and also check if chat already exists in minimized 
            chats and only can have 3 minimized chats
            */
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
        closeActiveChat: (state, action: PayloadAction<UserType>) => {
            // only remove from active chats
            state.active_chats = state.active_chats.filter((chat) => chat.user.id !== action.payload.id);
        },
        closeMinimizedChat: (state, action: PayloadAction<UserType>) => {
            // only remove from minimized chats
            state.minimized_chats = state.minimized_chats.filter((chat) => chat.user.id !== action.payload.id);
        },
        addNewUser: (state, action: PayloadAction<UserType>) => {
            // if user already exists, do nothing
            if(state.users.some((user) => user.id === action.payload.id)) return;
            state.users = [action.payload, ...state.users];
        },
        removeUser: (state, action: PayloadAction<UserType>) => {
            state.users = state.users.filter((user) => user.id !== action.payload.id);
        },
        addMessage: (state, action: PayloadAction<{ user: UserType, message: MessageType }>) => {
            // add message to chat and if chat is minimized, increase new_messages count and also add msg to active chat
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
        minimizeActiveChat: (state, action: PayloadAction<UserType>) => {
            // remove chat from active chats and add to minimized chats
            const chat = state.active_chats.find((chat) => chat.user.id === action.payload.id);
            if(!chat) return;
            state.active_chats = state.active_chats.filter((chat) => chat.user.id !== action.payload.id);
            state.minimized_chats = [chat, ...state.minimized_chats];
        },
        openMinimizedChat: (state, action: PayloadAction<UserType>) => {
            // remove chat from minimized chats and add to active chats. and update is_opened to true
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
        toggleActiveChat: (state, action: PayloadAction<UserType>) => {
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

	},
});

export const { addMessage, addNewUser, closeActiveChat, closeMinimizedChat, createNewChat, minimizeActiveChat, openMinimizedChat, removeUser, toggleActiveChat } = chatSlice.actions;
export default chatSlice.reducer;