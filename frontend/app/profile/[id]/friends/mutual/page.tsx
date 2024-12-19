"use client";
import FriendObject, { FriendObjectDummy } from "@/app/components/FriendObject";
import { apiClientFriends } from "@/data/api";
import { useInPageEndFunctionCalling } from "@/data/hooks";
import { RootState } from "@/data/stores";
import { UserType, ListResponseType } from "@/types/types";
import { useParams, useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";

function page() {
    const authUser = useSelector((state: RootState) => state.auth);
    const router = useRouter();
    const [loading, setLoading] = useState<boolean>(true);
    const [friends, setFriends] = useState<UserType[]>([]);
    const [next, setNext] = useState<string | null>(null);
    const params = useParams<{ id: string }>();

    async function getMutualFriends(link: string | null = `/users/${params.id}/friends/mutual/`) {
        if (!link) return;
        setLoading(true);
        await apiClientFriends
            .get(link)
            .then((res) => {
                const data = res.data as ListResponseType<UserType>;
                setFriends([...friends, ...data.results]);
                setNext(res.data.next);
            })
            .catch((err) => {
                console.log(err);
            });
        setLoading(false);
    }

    function updateFriend(user: UserType) {
        setFriends(friends.map((friend) => (friend.id === user.id ? user : friend)));
    }

    async function getNextMutualFriends() {
        if (!next) return;
        await getMutualFriends(next);
    }

    const lastPostRef = useInPageEndFunctionCalling({
        loading: loading,
        hasMore: Boolean(next),
        getNextList: getNextMutualFriends,
    });

    useEffect(() => {
        if (params.id === authUser.id) {
            router.push(`/profile/${authUser.id}/friends`);
        } else {
            getMutualFriends();
        }
    }, []);

    return (
        <div className="w-full grid grid-cols-2 gap-2 mt-2 pb-52">
            {friends.map((friend, index) => {
                if (friends.length === index + 1) {
                    return (
                        <FriendObject
                            removeUser={() => {}}
                            updateUser={updateFriend}
                            style="line"
                            user={friend}
                            key={friend.id}
                            ref={lastPostRef}
                        />
                    );
                } else {
                    return (
                        <FriendObject
                            removeUser={() => {}}
                            updateUser={updateFriend}
                            style="line"
                            user={friend}
                            key={friend.id}
                        />
                    );
                }
            })}
            {friends.length === 0 && !loading ? (
                <div className="w-full py-4">
                    <h1 className="text-xl">No mutual friends</h1>
                </div>
            ) : null}
            {loading
                ? Array.from({ length: 12 }).map((_, index) => <FriendObjectDummy style="line" key={index} />)
                : null}
        </div>
    );
}

export default page;
