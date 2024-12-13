"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import React, { useEffect } from "react";

function FriendsNavBar() {
    const pathname = usePathname();
    const [navList, setNavList] = React.useState([
        {
            name: "Friend Suggestions",
            url: "/friends",
            is_active: true,
        },
        {
            name: "Received Friend Requests",
            url: "/friends/received",
            is_active: false,
        },
        {
            name: "Sent Friend Requests",
            url: "/friends/sent",
            is_active: false,
        },
        {
            name: "All Friends",
            url: "/friends/all",
            is_active: false,
        },
    ]);

    useEffect(() => {
        setNavList((navList) =>
            navList.map((nav) => ({
                ...nav,
                is_active: nav.url === pathname,
            }))
        );
    }, [pathname]);

    return (
        <nav className="fixed pt-[7vh] top-0 bottom-0 left-0 h-screen w-[250px] bg-neutral-800 shadow-lg rounded-b-md">
            <ul className="w-full py-4 px-2">
                {navList.map((nav, index) => (
                    <li key={index} className="my-1">
                        <Link
                            href={nav.url}
                            className={`block px-4 py-2 rounded-md text-white hover:bg-neutral-700 ${
                                nav.is_active ? "bg-neutral-700" : ""
                            }`}
                        >
                            {nav.name}
                        </Link>
                    </li>
                ))}
            </ul>
        </nav>
    );
}

function layout({ children }: { children: React.ReactNode }) {
    return (
        <div className="pt-[7vh] flex justify-center">
            <div className="w-[800px]">
                <FriendsNavBar />
                <div className="w-full py-4">{children}</div>
            </div>
        </div>
    );
}

export default layout;
