import { TokensType, UserType } from '@/types/types';
import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import { storeUserTokens, clearUserTokens } from './funcs';

export type AuthType = {
	id: string;
	full_name: string;
	token: TokensType;
	isAuthenticated: boolean;
};

const initialState: AuthType = {
	id: '',
	full_name: '',
	token: {
		access: '',
		refresh: '',
	},
	isAuthenticated: false,
};

export const authSlice = createSlice({
	name: 'auth',
	initialState,
	reducers: {
		login: (state, action: PayloadAction<TokensType>) => {
			state.token = action.payload;
			state.isAuthenticated = true;
			storeUserTokens(action.payload);
		},
		logout: (state) => {
			state.id = '';
			state.full_name = '';
			state.token = {
				access: '',
				refresh: '',
			};
			state.isAuthenticated = false;
			clearUserTokens();
		},
		setUserData: (state, action: PayloadAction<UserType>) => {
			state.id = action.payload.id;
			state.full_name = action.payload.full_name;
		},
	},
});

export const { login, logout, setUserData } = authSlice.actions;
export default authSlice.reducer;
