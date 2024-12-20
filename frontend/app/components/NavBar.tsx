"use client";
import Link from "next/link";
import React, { useEffect, useState } from "react";
import Groups2OutlinedIcon from "@mui/icons-material/Groups2Outlined";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import { usePathname } from "next/navigation";
import { useSelector } from "react-redux";
import { RootState } from "@/data/stores";
import ChatComponents from "./ChatComponents";

function NavBar() {
    const request_count = useSelector((state: RootState) => state.auth.request_count);
    const [navList, setNavList] = useState([
        {
            name: "Home",
            icon: <HomeOutlinedIcon className="mr-4 text-2xl" />,
            href: "/",
            active: true,
        },
        {
            name: "Friends",
            icon: <Groups2OutlinedIcon className="mr-4 text-2xl" />,
            href: "/friends",
            active: false,
        },
    ]);
    const pathname = usePathname();
    const authUser = useSelector((state: RootState) => state.auth);
    const navIcon = authUser.full_name[0].toUpperCase();

    useEffect(() => {
        setNavList((prev) => {
            return prev.map((nav) => {
                if (nav.href === pathname) {
                    return { ...nav, active: true };
                } else if (nav.href === "/friends" && pathname.split("/")[1] === "friends") {
                    return { ...nav, active: true };
                }
                return { ...nav, active: false };
            });
        });
    }, [pathname]);

    return (
        <>
            <nav className="w-full h-[7vh] z-50 border-b border-neutral-700 bg-neutral-800 flex items-center px-6 justify-between fixed top-0 left-0 right-0">
                <div className="flex">
                    <Link
                        href={"/"}
                        className="relative w-[5vh] h-[5vh] bg-blue-600 rounded-full flex justify-center items-center overflow-hidden"
                    >
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
                                            nav.active
                                                ? "border-blue-600 text-blue-600 font-medium"
                                                : "border-transparent text-neutral-400"
                                        } cursor-pointer`}
                                    >
                                        {nav.icon}
                                        {nav.name}
                                        {nav.href === "/friends" && request_count > 0 ? (
                                            <span className="ml-2 bg-red-600 text-[12px] font-semibold p-1 text-white flex justify-center items-center rounded-full">
                                                {request_count > 99 ? "99+" : request_count}
                                            </span>
                                        ) : null}
                                    </div>
                                </Link>
                            </li>
                        );
                    })}
                </ul>
                <div>
                    <Link href={`/profile/${authUser.id}`}>
                        <h1 className="w-[5vh] h-[5vh] bg-neutral-500 text-2xl font-semibold rounded-full flex justify-center items-center">
                            {navIcon}
                        </h1>
                    </Link>
                </div>
            </nav>
            <ChatComponents />
        </>
    );
}

export default NavBar;
