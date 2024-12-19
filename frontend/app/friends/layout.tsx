"use client";
import { RootState } from "@/data/stores";
import Link from "next/link";
import { usePathname } from "next/navigation";
import React, { useEffect } from "react";
import { useSelector } from "react-redux";

function FriendsNavBar() {
    const authUser = useSelector((state: RootState) => state.auth);
    const request_count = useSelector((state: RootState) => state.auth.request_count);
    const pathname = usePathname();
    const [navList, setNavList] = React.useState([
        {
            name: "Friend Suggestions",
            url: "/friends",
            is_active: true,
        },
        {
            name: "Friend Requests",
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
            url: `/profile/${authUser.id}/friends`,
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
        <nav className="fixed pt-[7vh] top-0 bottom-0 left-0 h-screen w-[280px] bg-neutral-800 shadow-lg rounded-b-md">
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
                            {nav.url === "/friends/received" && request_count > 0 && (
                                <span className="ml-1 bg-red-500 text-white text-[10px] p-1 font-semibold rounded-full">
                                    {request_count > 99 ? "99+" : request_count}
                                </span>
                            )}
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
