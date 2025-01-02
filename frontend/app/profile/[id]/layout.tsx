"use client";
import { apiClientFriends } from "@/data/api";
import { UserType } from "@/types/types";
import React, { useEffect, useState } from "react";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import AddFreindIcon from "@mui/icons-material/PersonAddAlt1";
import CheckIcon from "@mui/icons-material/Check";
import PersonIcon from "@mui/icons-material/Person";
import ArrowForwardOutlinedIcon from "@mui/icons-material/ArrowForwardOutlined";
import ArrowBackOutlinedIcon from "@mui/icons-material/ArrowBackOutlined";
import Link from "next/link";
import { useSelector } from "react-redux";
import { RootState } from "@/data/stores";
import { useParams, usePathname } from "next/navigation";

function UserNotFound() {
    return (
        <div className="w-screen h-screen flex items-center justify-center">
            <div className="flex flex-col items-center">
                <h1 className="text-neutral-400 text-5xl font-light tracking-wider">404 User not found</h1>
                <Link href="/" className="px-4 py-2 rounded-md bg-blue-600 text-white mt-4">
                    <HomeOutlinedIcon className="mr-2" />
                    Home
                </Link>
            </div>
        </div>
    );
}

function FriendButton({
    user,
    updateUser,
}: {
    user: UserType;
    updateUser: React.Dispatch<React.SetStateAction<UserType | null>>;
}) {
    const authUser = useSelector((state: RootState) => state.auth);

    async function sendFriendRequest() {
        await apiClientFriends
            .post("/users/friends/requests/", { user_to_id: user.id })
            .then((res) => {
                updateUser({ ...user, sent_request: true, req_id: res.data.req_id });
            })
            .catch((err) => {
                console.error(err);
            });
    }

    async function cancelFriendRequest() {
        await apiClientFriends
            .post(`/users/friends/requests/action/`, { request_id: user.req_id, action: "reject" })
            .then((res) => {
                updateUser({ ...user, sent_request: false });
            })
            .catch((err) => {
                console.error(err);
            });
    }

    async function confirmFriendRequest() {
        await apiClientFriends
            .post("/users/friends/requests/action/", { request_id: user.req_id, action: "accept" })
            .then((res) => {
                updateUser({ ...user, is_friend: true, sent_request: false, received_request: false });
            })
            .catch((err) => {
                console.error(err);
            });
    }

    if (user.is_friend) {
        return (
            <button className="bg-blue-500 px-6 py-2 rounded-md text-white flex items-center">
                <span className="relative">
                    <PersonIcon className="mr-2" />
                    <CheckIcon className="absolute top-1 right-1" sx={{ fontSize: 12 }} />
                </span>
                Friends
            </button>
        );
    }
    if (user.id === authUser.id) {
        return null;
    }
    if (user.sent_request) {
        return (
            <div>
                <button
                    className="bg-blue-500 px-6 py-2 rounded-md text-white flex items-center"
                    onClick={cancelFriendRequest}
                >
                    <span className="relative">
                        <PersonIcon className="mr-2" />
                        <ArrowForwardOutlinedIcon className="absolute top-1 right-1" sx={{ fontSize: 12 }} />
                    </span>
                    Request Sent
                </button>
            </div>
        );
    }
    if (user.received_request) {
        return (
            <div>
                <button
                    className="bg-blue-500 px-6 py-2 rounded-md text-white flex items-center"
                    onClick={confirmFriendRequest}
                >
                    <span className="relative">
                        <PersonIcon className="mr-2" />
                        <ArrowBackOutlinedIcon className="absolute top-1 right-1" sx={{ fontSize: 12 }} />
                    </span>
                    Accept Request
                </button>
            </div>
        );
    }

    return (
        <button className="bg-blue-500 px-6 py-2 rounded-md text-white flex items-center" onClick={sendFriendRequest}>
            <AddFreindIcon className="mr-2" />
            Add Friend
        </button>
    );
}

function PageButtons({ user }: { user: UserType }) {
    const authUser = useSelector((state: RootState) => state.auth);
    const pathname = usePathname();
    const [navItems, setNavItems] = useState([
        { name: "Posts", link: `/profile/${user.id}`, active: true },
        { name: "All Friends", link: `/profile/${user.id}/friends`, active: false },
        { name: "Mutual Friends", link: `/profile/${user.id}/friends/mutual`, active: false },
    ]);

    useEffect(() => {
        setNavItems(
            navItems.map((navItem) => {
                if (navItem.link === pathname) {
                    return { ...navItem, active: true };
                } else {
                    return { ...navItem, active: false };
                }
            })
        );
    }, [pathname]);

    return (
        <ul className="flex w-full px-6 pt-1 bg-neutral-800 gap-2">
            {navItems.map((navItem, index) =>
                authUser.id === user.id && navItem.link === `/profile/${user.id}/friends/mutual` ? null : (
                    <Link
                        key={index}
                        href={navItem.link}
                        className={`border-b-2 ${navItem.active ? "border-b-blue-700" : "border-b-neutral-800"}`}
                    >
                        <li
                            className={`px-4 py-2 rounded-md text-white ${
                                navItem.active ? "" : "hover:bg-neutral-700"
                            }`}
                        >
                            {navItem.name}
                        </li>
                    </Link>
                )
            )}
        </ul>
    );
}

function layout({ children }: { children: React.ReactNode }) {
    const params = useParams<{ id: string }>();
    const [user, setUser] = useState<UserType | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const authUser = useSelector((state: RootState) => state.auth);

    async function getUserProfile() {
        if (!params.id) return;
        setLoading(true);
        await apiClientFriends
            .get(`/users/${params.id}/`)
            .then((res) => {
                setUser(res.data);
            })
            .catch((err) => {
                console.log(err);
            });
        setLoading(false);
    }

    useEffect(() => {
        getUserProfile();
    }, []);

    if (loading) {
        return null;
    }

    return (
        <>
            {!user ? (
                <UserNotFound />
            ) : (
                <div className="flex flex-col items-center w-full mt-[7vh]">
                    <div className="max-w-[1000px] w-[1000px] px-4 bg-neutral-600 rounded-b-lg">
                        <div className="flex items-center gap-4">
                            <div className="w-36 h-36 translate-y-[30%] rounded-full bg-red-500 text-[60px] flex items-center justify-center">
                                {user.full_name
                                    .trim()
                                    .split(" ")
                                    .map((name) => name[0].toUpperCase())}
                            </div>
                            <div className="flex justify-between w-4/5 translate-y-[90%]">
                                <h1 className="text-white text-3xl font-medium">{user.full_name}</h1>
                                <FriendButton user={user} updateUser={setUser} />
                            </div>
                        </div>
                    </div>
                    <div className="w-[700px]">
                        <PageButtons user={user} />
                        {children}
                    </div>
                </div>
            )}
        </>
    );
}

export default layout;
