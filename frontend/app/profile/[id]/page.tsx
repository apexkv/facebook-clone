'use client';
import { apiClientUser } from '@/data/api';
import { UserType } from '@/types/types';
import React, { useEffect, useState } from 'react';

function UserNotFound() {
	return (
		<div>
			<h1>User not found</h1>
		</div>
	);
}

function Profile({ params }: { params: { id: string } }) {
	const [profileId, setProfileId] = useState<string | null>(null);
	const [user, setUser] = useState<UserType | null>(null);
	const [loading, setLoading] = useState<boolean>(true);

	async function getUserProfile() {
		if (!profileId) return;
		setLoading(true);
		await apiClientUser
			.get(`${profileId}/`)
			.then((res) => {
				setUser(res.data);
			})
			.catch((err) => {
				console.log(err);
			});
		setLoading(false);
	}

	useEffect(() => {
		async function unwrapParams() {
			const unwrappedParams = await params;
			setProfileId(unwrappedParams.id);
		}
		unwrapParams();
	}, [params]);

	useEffect(() => {
		getUserProfile();
	}, [profileId]);

	if (loading) {
		return (
			<div>
				<h1>Loading...</h1>
			</div>
		);
	}

	return (
		<>
			{!user ? (
				<UserNotFound />
			) : (
				<div>
					<h1>Profile {user.full_name}</h1>
				</div>
			)}
		</>
	);
}

export default Profile;
