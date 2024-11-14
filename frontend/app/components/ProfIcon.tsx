'use client';
import Link from 'next/link';
import React from 'react';

const bgColors = ['bg-red-600', 'bg-blue-600', 'bg-green-600', 'bg-yellow-600', 'bg-indigo-600', 'bg-purple-600', 'bg-pink-600'];
// const randomBgColor = bgColors[2];
function ProfIcon({ name, userId, size = 5 }: { name: string; userId: string; size?: number }) {
	const firstLetter = name[0].toUpperCase();
	const randomBgColor = bgColors[Math.floor(Math.random() * bgColors.length)];
	return (
		<Link href={`/profile/${userId}`}>
			<h1
				className={`${randomBgColor} rounded-full ${size > 4 ? 'w-14' : 'w-10'} ${size > 4 ? 'h-14' : 'h-10'} font-semibold text-${
					size > 4 ? 2 : ''
				}xl flex items-center justify-center`}
			>
				{firstLetter}
			</h1>
		</Link>
	);
}

export default ProfIcon;
