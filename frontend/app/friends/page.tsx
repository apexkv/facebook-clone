"use client";
import React, { useEffect } from "react";
import FriendObject, { FriendObjectDummy } from "../components/FriendObject";
import { UserType } from "@/types/types";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "@/data/stores";
import { useInPageEndFunctionCalling } from "@/data/hooks";
import { getFriendSuggestions, getNextFriendSuggestions } from "@/data/funcs";
import { removeFriend, updateFriend } from "@/data/friends_slice";

function Friends() {
    const friends = useSelector((state: RootState) => state.friends.friends);
    const loading = useSelector((state: RootState) => state.friends.loading);
    const next_link = useSelector((state: RootState) => state.friends.next_link);
    const dispatch = useDispatch();

    const lastPostRef = useInPageEndFunctionCalling({
        loading: loading,
        hasMore: Boolean(next_link),
        getNextList: getNextFriendSuggestions,
    });

    function removeFriendObject(id: string) {
        dispatch(removeFriend(id));
    }

    function updateFriendObject(user: UserType) {
        dispatch(updateFriend(user));
    }

    useEffect(() => {
        if (friends.length === 0) {
            getFriendSuggestions();
        }
    }, []);

    return (
        <div>
            <h1 className="text-2xl mb-6 font-bold">You may Know</h1>
            <div className="w-full grid grid-cols-4 gap-3">
                {friends.map((friend: UserType, index: number) => {
                    if (friends.length === index + 1) {
                        return (
                            <FriendObject
                                removeUser={removeFriendObject}
                                updateUser={updateFriendObject}
                                user={friend}
                                key={friend.id}
                                ref={lastPostRef}
                            />
                        );
                    } else {
                        return (
                            <FriendObject
                                removeUser={removeFriendObject}
                                updateUser={updateFriendObject}
                                user={friend}
                                key={friend.id}
                            />
                        );
                    }
                })}
                {loading ? Array.from({ length: 12 }).map((_, index) => <FriendObjectDummy key={index} />) : null}
            </div>
        </div>
    );
}

export default Friends;
