import { UserType } from '@/types/types';
import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export type FriendSuggestionListType = {
	friends: UserType[];
    next_link: string | null;
    loading: boolean;
    error: string | null;
};

const initialState: FriendSuggestionListType = {
    friends: [],
    next_link: null,
    loading: true,
    error: null,
};

export const friendsSlice = createSlice({
	name: 'friends',
	initialState,
	reducers: {
		addFriendList: (state, action: PayloadAction<UserType[]>) => {
            state.friends = state.friends.concat(action.payload.filter(friend => !state.friends.some(f => f.id === friend.id)));
        },
        setNextLink: (state, action: PayloadAction<string | null>) => {
            state.next_link = action.payload;
        },
        setLoading: (state, action: PayloadAction<boolean>) => {
            state.loading = action.payload;
        },
        setError: (state, action: PayloadAction<string | null>) => {
            state.error = action.payload
        },
        removeFriend: (state, action: PayloadAction<string>) => {
            console.log("Removing friend with ID:", action.payload);
            console.log("Current friends list:", state.friends);

            state.friends = state.friends.filter(friend => friend.id !== action.payload);

            console.log("Updated friends list:", state.friends);
        },
        updateFriend: (state, action: PayloadAction<UserType>) => {
            state.friends = state.friends.map(friend => {
                if (friend.id === action.payload.id) {
                    return action.payload;
                }
                return friend;
            });
        }
	},
});

export const { addFriendList, setNextLink, setError, setLoading, removeFriend, updateFriend } = friendsSlice.actions;
export default friendsSlice.reducer;