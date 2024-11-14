import axios, { InternalAxiosRequestConfig } from 'axios';
import { getUserTokens, storeUserTokens } from './funcs';
import { TokensType } from '@/types/types';

const USER_API_URL = 'http://localhost:8010/api/users/';
const POST_API_URL = 'http://localhost:8020/api/postwrite/';
const FRIENDS_API_URL = 'http://localhost:8030/api/friendship/';

function isTokenExpired(token: string) {
	try {
		const payload = JSON.parse(atob(token.split('.')[1]));

		if (!payload.exp) {
			return false;
		}

		const currentTime = Math.floor(Date.now() / 1000);

		return currentTime >= payload.exp;
	} catch (error) {
		console.error('Invalid token', error);
		return true;
	}
}

async function apiInterceptor(config: InternalAxiosRequestConfig<any>) {
	const token = getUserTokens();
	if (token) {
		const isExpired = isTokenExpired(token.access);

		if (!isExpired) {
			config.headers.Authorization = `JWT ${token.access}`;
		} else {
			try {
				const response = await axios.post(`${USER_API_URL}refresh/`, {
					refresh: token.refresh,
				});
				const newTokens = response.data as TokensType;
				storeUserTokens(newTokens);
				config.headers.Authorization = `JWT ${newTokens.access}`;
			} catch (error) {
				console.error('Invalid token', error);
			}
		}
	}

	return config;
}

const apiClientUser = axios.create({
	baseURL: USER_API_URL,
	headers: {
		'Content-Type': 'application/json',
	},
});

const apiClientPost = axios.create({
	baseURL: POST_API_URL,
	headers: {
		'Content-Type': 'application/json',
	},
});

const apiClientFriends = axios.create({
	baseURL: FRIENDS_API_URL,
	headers: {
		'Content-Type': 'application/json',
	},
});

apiClientUser.interceptors.request.use(apiInterceptor);
apiClientPost.interceptors.request.use(apiInterceptor);
apiClientFriends.interceptors.request.use(apiInterceptor);

export { apiClientUser, apiClientPost, apiClientFriends };
