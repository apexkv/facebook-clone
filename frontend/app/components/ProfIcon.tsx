import Link from 'next/link';
import React from 'react';

function ProfIcon({ name, href, size = 5 }: { name: string; href: string; size?: number }) {
	const firstLetter = name[0].toUpperCase();
	const bgColors = ['bg-red-600', 'bg-blue-600', 'bg-green-600', 'bg-yellow-600', 'bg-indigo-600', 'bg-purple-600', 'bg-pink-600'];
	const randomBgColor = bgColors[Math.floor(Math.random() * bgColors.length)];
	return (
		<Link href={href}>
			<h1 className={`${randomBgColor} rounded-full w-[${size}vh] h-[${size}vh] font-medium text-${size > 4 ? 2 : 1}xl flex items-center justify-center`}>{firstLetter}</h1>
		</Link>
	);
}

export default ProfIcon;
