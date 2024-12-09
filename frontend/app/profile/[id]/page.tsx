"use client";
import { apiClientUser } from "@/data/api";
import { UserType } from "@/types/types";
import React, { useEffect, useState } from "react";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import Link from "next/link";
import { PostCreate, PostsLoadingDummySet } from "@/app/components/PostContainer";
import { useApiGetPostList, useInPageEndFunctionCalling } from "@/data/hooks";
import Post from "@/app/components/Post";
import { useSelector } from "react-redux";
import { RootState } from "@/data/stores";
import { useParams } from "next/navigation";

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

function Profile() {
    const params = useParams<{ id: string }>();
    const [user, setUser] = useState<UserType | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const authUser = useSelector((state: RootState) => state.auth);

    async function getUserProfile() {
        if (!params.id) return;
        setLoading(true);
        await apiClientUser
            .get(`${params.id}/`)
            .then((res) => {
                setUser(res.data);
            })
            .catch((err) => {
                console.log(err);
            });
        setLoading(false);
    }

    const { postList, loading: loadingPostList, getList, getNextList, hasMore } = useApiGetPostList(params.id);
    const lastPostRef = useInPageEndFunctionCalling({ loading, hasMore, getNextList });

    useEffect(() => {
        getUserProfile();
        getList();
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
                        <div className="flex translate-y-[30%] items-center gap-4">
                            <div className="w-36 h-36 rounded-full bg-red-500 text-[60px] flex items-center justify-center">
                                {user.full_name
                                    .trim()
                                    .split(" ")
                                    .map((name) => name[0].toUpperCase())}
                            </div>
                            <h1 className="text-white text-3xl font-medium">{user.full_name}</h1>
                        </div>
                    </div>
                    <div className="w-[700px]">
                        {authUser.id === user.id ? <PostCreate /> : null}
                        {postList.map((post, index) => {
                            if (postList.length === index + 1) {
                                return <Post key={index} post={post} ref={lastPostRef} isFromFeed={false} />;
                            } else {
                                return <Post key={index} post={post} isFromFeed={false} />;
                            }
                        })}
                        {loadingPostList ? <PostsLoadingDummySet /> : null}
                    </div>
                </div>
            )}
        </>
    );
}

export default Profile;
