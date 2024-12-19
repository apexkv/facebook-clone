"use client";
import FriendObject, { FriendObjectDummy } from "@/app/components/FriendObject";
import { apiClientFriends } from "@/data/api";
import { useInPageEndFunctionCalling } from "@/data/hooks";
import { ListResponseType, UserType } from "@/types/types";
import React, { useEffect, useState } from "react";

function page() {
    const [requestList, setRequestList] = useState<UserType[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<null | string>(null);
    const [next_link, setNextLink] = useState<string | null>(null);

    async function getRequests(link: string | null = "users/friends/requests/") {
        if (!link) return;
        setLoading(true);
        await apiClientFriends
            .get(link)
            .then((res) => {
                const data = res.data as ListResponseType<UserType>;
                setRequestList([...requestList, ...data.results]);
                setNextLink(data.next);
            })
            .catch((err) => {
                console.log(err);
            })
            .finally(() => {
                setLoading(false);
            });
    }

    async function getNextFriendReuqests() {
        if (!next_link) return;
        await getRequests(next_link);
    }

    const lastPostRef = useInPageEndFunctionCalling({
        loading: loading,
        hasMore: Boolean(next_link),
        getNextList: getNextFriendReuqests,
    });

    function removeFriend(id: string) {
        setRequestList(requestList.filter((request) => request.id !== id));
    }

    function updateFriend(user: UserType) {
        setRequestList(requestList.map((request) => (request.id === user.id ? user : request)));
    }

    useEffect(() => {
        getRequests();
    }, []);

    return (
        <div className="w-full">
            <h1 className="mb-4">Recieved Friend Request</h1>
            <div className="w-full grid grid-cols-2 gap-2">
                {requestList.map((request, index) => {
                    if (requestList.length === index + 1) {
                        return (
                            <FriendObject
                                removeUser={removeFriend}
                                updateUser={updateFriend}
                                style="line"
                                user={request}
                                key={request.id}
                                ref={lastPostRef}
                            />
                        );
                    } else {
                        return (
                            <FriendObject
                                removeUser={removeFriend}
                                updateUser={updateFriend}
                                style="line"
                                user={request}
                                key={request.id}
                            />
                        );
                    }
                })}
                {loading
                    ? Array.from({ length: 12 }).map((_, index) => <FriendObjectDummy style="line" key={index} />)
                    : null}
            </div>
        </div>
    );
}

export default page;
