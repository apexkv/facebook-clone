import { TokensType } from '@/types/types';

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
