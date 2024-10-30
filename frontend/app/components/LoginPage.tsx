import Link from 'next/link';
import React from 'react';
import Hr from './Hr';

function LoginPage() {
	return (
		<div className="flex flex-col justify-center h-screen items-center bg-slate-200">
			<div className="flex w-max-[1000px] w-[1000px]">
				<div className="w-1/2 flex items-center">
					<div>
						<h1 className="text-6xl font-bold text-blue-600">facebook-clone</h1>
						<p className="text-2xl font-medium">Facebook helps you connect and share with the people in your life.</p>
					</div>
				</div>
				<div className="w-1/2 flex items-center justify-end">
					<div className="w-4/5 bg-white shadow-xl rounded-lg p-4">
						<form className="w-full flex flex-col items-center">
							<input type="email" className="w-full border p-4 text-xl rounded-md mb-4" placeholder="Email" autoComplete="email" />
							<input type="password" className="w-full border p-4 text-xl rounded-md mb-4" placeholder="Password" autoComplete="current-password" />
							<button className="w-full p-3 bg-blue-600 text-xl font-medium rounded-md text-white">Log in</button>
							<Hr color="bg-black" my={8} />
							<Link href={'/register'} className="bg-green-500 font-medium text-white px-8 py-3 rounded-md">
								Create new account
							</Link>
						</form>
					</div>
				</div>
			</div>
			<div className="h-56" />
		</div>
	);
}

export default LoginPage;
