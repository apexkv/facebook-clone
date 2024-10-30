'use client';
import React, { useState } from 'react';
import NavBar from './NavBar';
import LoginPage from './LoginPage';

function AuthProvider({ children }: { children: React.ReactNode }) {
	const [isLoggedIn, setIsLoggedIn] = useState<boolean>(true);
	return (
		<>
			{isLoggedIn ? (
				<>
					<NavBar />
					<div className="!text-white">{children}</div>
				</>
			) : (
				<LoginPage />
			)}
		</>
	);
}

export default AuthProvider;
