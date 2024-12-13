"use client";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Skeleton } from "@mui/material";
import { UserType } from "@/types/types";
import { apiClientFriends } from "@/data/api";
import { useDispatch } from "react-redux";
import { removeFriend, updateFreiend } from "@/data/friends_slice";

type FriendObjectType = {
    user: UserType;
    style?: "line" | "block";
    ref?: React.LegacyRef<HTMLDivElement>;
};

export function FriendObjectDummy() {
    return (
        <div className={`w-full border border-neutral-600 rounded-lg overflow-hidden bg-neutral-800`}>
            <Skeleton variant="rectangular" className="w-full !h-40" sx={{ bgcolor: "grey.800" }} />
            <div className="p-2">
                <Skeleton variant="text" className="w-4/5 !h-7 mb-1" sx={{ bgcolor: "grey.800" }} />
                <div className="h-8">
                    <Skeleton variant="text" className="w-2/3 !h-5 mb-2" sx={{ bgcolor: "grey.800" }} />
                </div>
                <Skeleton variant="rectangular" className="w-full !h-10 rounded-md my-2" sx={{ bgcolor: "grey.800" }} />
                <Skeleton variant="rectangular" className="w-full !h-10 rounded-md" sx={{ bgcolor: "grey.800" }} />
            </div>
        </div>
    );
}

function FriendObject({ user, style = "block", ref }: FriendObjectType) {
    const randomColor = Math.floor(Math.random() * 16777215).toString(16);
    const f1bg = Math.floor(Math.random() * 16777215).toString(16);
    const f2bg = Math.floor(Math.random() * 16777215).toString(16);

    const dispatch = useDispatch();
    const [requestCanceled, setRequestCanceled] = useState(false);

    async function sendFriendRequest() {
        await apiClientFriends
            .post("/users/friends/requests/", { user_to_id: user.id })
            .then((res) => {
                dispatch(updateFreiend({ ...user, sent_request: true }));
            })
            .catch((err) => {
                console.error(err);
            });
    }

    async function cancelFriendRequest() {
        await apiClientFriends
            .delete(`/users/friends/requests/${user.id}/`)
            .then((res) => {
                dispatch(updateFreiend({ ...user, sent_request: false }));
                setRequestCanceled(true);
            })
            .catch((err) => {
                console.error(err);
            });
    }

    async function removeUser() {
        await apiClientFriends
            .delete(`/suggestions/${user.id}/`)
            .then((res) => {
                dispatch(removeFriend(user.id));
            })
            .catch((err) => {
                console.error(err);
            });
    }

    return (
        <div className={`w-full border border-neutral-600 rounded-lg bg-neutral-800`} ref={ref}>
            <Link
                href={`/profile/${user.id}`}
                style={{ backgroundColor: `#${randomColor}` }}
                className={`w-full h-40 flex justify-center items-center rounded-t-lg`}
            >
                <h1 className="text-6xl">
                    {user.full_name
                        .trim()
                        .split(" ")
                        .map((name) => name[0].toUpperCase())}
                </h1>
            </Link>
            <div className="p-2">
                <Link href={`/profile/${user.id}`} className="w-full">
                    <h1 className="text-lg font-semibold truncate">{user.full_name}</h1>
                </Link>
                <div className="h-8">
                    <div className="flex items-center">
                        <span className="relative w-[30px]">
                            {user.mutual_friends_list.length > 0 && (
                                <Link href={`/profile/${user.mutual_friends_list[0].id}`}>
                                    <h4
                                        className="w-4 h-4 rounded-full bg-green-800 font-bold flex justify-center items-center shadow-md"
                                        style={{ fontSize: 12, backgroundColor: `#${f1bg}` }}
                                    >
                                        {user.mutual_friends_list[0].full_name[0].slice(0, 1).toUpperCase()}
                                    </h4>
                                </Link>
                            )}
                            {user.mutual_friends_list.length > 1 && (
                                <Link
                                    href={`/profile/${user.mutual_friends_list[1].id}`}
                                    className="absolute left-3 top-0"
                                >
                                    <h4
                                        className="w-4 h-4 rounded-full bg-green-800 font-bold flex justify-center items-center shadow-md"
                                        style={{ fontSize: 12, backgroundColor: `#${f2bg}` }}
                                    >
                                        {user.mutual_friends_list[1].full_name[0].slice(0, 1).toUpperCase()}
                                    </h4>
                                </Link>
                            )}
                        </span>
                        {user.mutual_friends > 0 && (
                            <span className="relative ml-2 group">
                                <h4 className="text-neutral-400 text-sm cursor-pointer">
                                    {user.mutual_friends} mutual friends
                                </h4>
                                <div
                                    className="absolute max-w-[200px] bg-[#f0f0f0e8] rounded-md p-2 z-50 text-black opacity-0 pointer-events-none group-hover:opacity-100 group-hover:pointer-events-auto transition-opacity duration-300"
                                    style={{ fontSize: 10 }}
                                >
                                    {user.mutual_friends_name_list.map((friend, index) => (
                                        <p key={index} className="whitespace-nowrap overflow-hidden text-ellipsis">
                                            {friend}
                                        </p>
                                    ))}
                                    {user.mutual_friends > user.mutual_friends_name_list.length && (
                                        <p className="whitespace-nowrap overflow-hidden text-ellipsis">
                                            and {user.mutual_friends - user.mutual_friends_name_list.length} more...
                                        </p>
                                    )}
                                </div>
                            </span>
                        )}
                    </div>
                    {!user.sent_request && requestCanceled ? (
                        <p className="text-neutral-400">Request Canceled</p>
                    ) : null}
                </div>
                <div className="w-full">
                    {user.sent_request ? (
                        <>
                            <div className="h-10 my-2" />
                            <button onClick={cancelFriendRequest} className="w-full rounded-md bg-neutral-600 py-2">
                                Cancel
                            </button>
                        </>
                    ) : (
                        <>
                            <button
                                onClick={sendFriendRequest}
                                className="w-full my-2 rounded-md bg-opacity-40 font-semibold bg-[#3b82f650] text-blue-400 py-2"
                            >
                                Add Friend
                            </button>
                            <button onClick={removeUser} className="w-full rounded-md bg-neutral-600 py-2">
                                Remove
                            </button>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}

export default FriendObject;
