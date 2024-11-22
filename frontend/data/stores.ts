import { configureStore } from '@reduxjs/toolkit';
import authSlice from '@/data/auth_slise';
import postSlice from '@/data/post_slice';

export const store = configureStore({
	reducer: {
		auth: authSlice,
		posts: postSlice,
	},
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
