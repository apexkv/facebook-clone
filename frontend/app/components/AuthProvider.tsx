'use client';
import React, { useEffect, useState } from 'react';
import { Provider, useDispatch, useSelector } from 'react-redux';
import NavBar from './NavBar';
import LoginPage from './LoginPage';
import { RootState, store } from '@/data/stores';
import { usePathname } from 'next/navigation';
import RegisterPage from './RegisterPage';
import { apiClientUser } from '@/data/api';
import { getUserTokens } from '@/data/funcs';
import { login, logout, setUserData } from '@/data/auth_slise';

function AuthHandler({ children }: { children: React.ReactNode }) {
	const dispatch = useDispatch();
	const [loading, setLoading] = useState<boolean>(true);

	async function validateToken() {
		setLoading(true);
		const token = getUserTokens();
		if (token) {
			await apiClientUser
				.get('/me/')
				.then((res) => {
					const newToken = getUserTokens();
					if (newToken) {
						dispatch(login(newToken));
						dispatch(setUserData(res.data));
					}
				})
				.catch((err) => {
					console.log(err);
					dispatch(logout());
				});
		}
		setLoading(false);
	}

	const authState = useSelector((state: RootState) => state.auth);
	const pathname = usePathname();

	useEffect(() => {
		validateToken();
	}, []);

	if (loading) {
		return null;
	}

	return (
		<>
			{authState.isAuthenticated ? (
				<>
					<NavBar />
					<div className="!text-white">{children}</div>
				</>
			) : pathname === '/login' || pathname === '/' ? (
				<LoginPage />
			) : (
				<RegisterPage />
			)}
		</>
	);
}

function AuthProvider({ children }: { children: React.ReactNode }) {
	return (
		<Provider store={store}>
			<AuthHandler>{children}</AuthHandler>
		</Provider>
	);
}

export default AuthProvider;
