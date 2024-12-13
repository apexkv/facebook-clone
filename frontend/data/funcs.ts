import { ListResponseType, TokensType, UserType } from '@/types/types';
import {store,RootState} from '@/data/stores'
import { addFriendList, setError, setLoading, setNextLink } from './friends_slice';
import { apiClientFriends } from './api';


export function postFormatTime(created_at: string): string {
	const currentTime = new Date();
	const createdTime = new Date(created_at);
	const diffInSeconds = Math.floor((currentTime.getTime() - createdTime.getTime()) / 1000);

	if (diffInSeconds < 60) {
		return `${diffInSeconds}s ago`;
	}

	const diffInMinutes = Math.floor(diffInSeconds / 60);
	if (diffInMinutes < 60) {
		return `${diffInMinutes}m ago`;
	}

	const diffInHours = Math.floor(diffInMinutes / 60);
	if (diffInHours < 24) {
		return `${diffInHours}h ago`;
	}

	const diffInDays = Math.floor(diffInHours / 24);
	if (diffInDays < 30) {
		return diffInDays === 1 ? 'a day ago' : `${diffInDays} days ago`;
	}

	const diffInMonths = currentTime.getMonth() - createdTime.getMonth() + 12 * (currentTime.getFullYear() - createdTime.getFullYear());
	if (diffInMonths < 12) {
		return createdTime.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
	}

	return createdTime.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
}

export function commentFormatTime(created_at: string): string {
	const currentTime = new Date();
	const createdTime = new Date(created_at);
	const diffInSeconds = Math.floor((currentTime.getTime() - createdTime.getTime()) / 1000);

	if (diffInSeconds < 60) {
		return `${diffInSeconds}s`;
	}

	const diffInMinutes = Math.floor(diffInSeconds / 60);
	if (diffInMinutes < 60) {
		return `${diffInMinutes}m`;
	}

	const diffInHours = Math.floor(diffInMinutes / 60);
	if (diffInHours < 24) {
		return `${diffInHours}h`;
	}

	const diffInDays = Math.floor(diffInHours / 24);
	if (diffInDays < 7) {
		return `${diffInDays}d`;
	}

	const diffInWeeks = Math.floor(diffInDays / 7);
	if (diffInWeeks < 52) {
		return `${diffInWeeks}w`;
	}

	const diffInYears = Math.floor(diffInWeeks / 52);
	return `${diffInYears}y`;
}

export const AUTH_TOKENS = 'FB_AUTH_TOKENS';

export function storeUserTokens(tokens: TokensType) {
	window.localStorage.setItem(AUTH_TOKENS, JSON.stringify(tokens));
}

export function getUserTokens() {
	const tokens = window.localStorage.getItem(AUTH_TOKENS);
	if (tokens) {
		return JSON.parse(tokens) as TokensType;
	}
	return null;
}

export function clearUserTokens() {
	window.localStorage.removeItem(AUTH_TOKENS);
}


export async function getFriendSuggestions(link: string | null = "/suggestions/"){
	if (!link) return;
		store.dispatch(setLoading(true))
		store.dispatch(setError(null))
		try {
			const res = await apiClientFriends.get(link);
			const responseData = res.data as ListResponseType<UserType>;
			store.dispatch(addFriendList(responseData.results))
			store.dispatch(setNextLink(responseData.next))
		} catch (err: any) {
			store.dispatch(setError(err.message || 'An error occurred'))
			console.error(err);
		} finally {
			store.dispatch(setLoading(false))
		}
}

export async function getNextFriendSuggestions(){
	const state = store.getState() as RootState;
	const {loading, next_link} = state.friends;
	if (loading || !next_link) return;
	await getFriendSuggestions(next_link);
}