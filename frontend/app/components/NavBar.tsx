'use client';
import Link from 'next/link';
import React, { useEffect, useState } from 'react';
import Groups2OutlinedIcon from '@mui/icons-material/Groups2Outlined';
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import { usePathname } from 'next/navigation';

function NavBar() {
	const [navList, setNavList] = useState([
		{
			name: 'Home',
			icon: <HomeOutlinedIcon className="mr-4 text-2xl" />,
			href: '/',
			active: true,
		},
		{
			name: 'Friends',
			icon: <Groups2OutlinedIcon className="mr-4 text-2xl" />,
			href: '/friends',
			active: false,
		},
	]);
	const pathname = usePathname();

	useEffect(() => {
		setNavList((prev) => {
			return prev.map((nav) => {
				if (nav.href === pathname) {
					return { ...nav, active: true };
				}
				return { ...nav, active: false };
			});
		});
	}, [pathname]);

	return (
		<nav className="w-full h-[7vh] border-b border-neutral-700 bg-neutral-800 flex items-center px-6 justify-between">
			<div className="flex">
				<Link href={'/'} className="relative w-[5vh] h-[5vh] bg-blue-600 rounded-full flex justify-center items-center overflow-hidden">
					<h1 className="text-6xl font-bold absolute -bottom-4">f</h1>
				</Link>
			</div>
			<ul className="flex items-center">
				{navList.map((nav) => {
					return (
						<li key={nav.name}>
							<Link href={nav.href}>
								<div
									className={`w-[150px] flex justify-center items-center h-[7vh] border-b-4 ${
										nav.active ? 'border-blue-600 text-blue-600 font-medium' : 'border-transparent text-neutral-400'
									} cursor-pointer`}
								>
									{nav.icon}
									{nav.name}
								</div>
							</Link>
						</li>
					);
				})}
			</ul>
			<div>
				<Link href={'/profile'}>
					<h1 className="w-[5vh] h-[5vh] bg-neutral-500 text-2xl rounded-full flex justify-center items-center">K</h1>
				</Link>
			</div>
		</nav>
	);
}

export default NavBar;
