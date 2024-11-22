"use client";
import React, { useEffect } from "react";
import { Skeleton } from "@mui/material";
import { Field, Form, Formik, FormikHelpers } from "formik";
import { useDispatch, useSelector } from "react-redux";
import * as Yup from "yup";
import Post from "./Post";
import Hr from "./Hr";
import ProfIcon from "./ProfIcon";
import { RootState } from "@/data/stores";
import { useApiGetPostList, useInPageEndFunctionCalling } from "@/data/hooks";
import { apiClientPost } from "@/data/api";
import { addPost } from "@/data/post_slice";
import { PostType } from "@/types/types";

function PostCreate() {
    const dispatch = useDispatch();
    const userData = useSelector((state: RootState) => state.auth);

    const postSchema = Yup.object().shape({
        content: Yup.string().required("Required"),
    });

    const initialValues = { content: "" };

    async function createPost(values: typeof initialValues, formikHelpers: FormikHelpers<typeof initialValues>) {
        await apiClientPost
            .post(`/`, { content: values.content })
            .then((res) => {
                const data = res.data as PostType;
                dispatch(addPost(data));
                formikHelpers.resetForm();
            })
            .catch((err) => {
                console.log(err);
            });
    }

    return (
        <div className="w-full bg-neutral-800 p-4 rounded-lg mt-4 ">
            <Formik initialValues={initialValues} onSubmit={createPost} className="mt-4" validationSchema={postSchema}>
                <Form>
                    <div className="flex justify-between">
                        <ProfIcon userId={userData.id} name={userData.full_name} />
                        <Field
                            type="textarea"
                            name="content"
                            placeholder={`What's on your mind, ${userData.full_name.split(" ")[0]}?`}
                            className="w-[90%] bg-neutral-700 rounded-[30px] text-lg outline-none px-6 py-4"
                            rows={1}
                        />
                    </div>
                    <Hr my={4} />
                    <button className="w-full py-2 text-base rounded-full font-medium text-blue-600 hover:bg-blue-600 hover:text-white">
                        Create Post
                    </button>
                </Form>
            </Formik>
        </div>
    );
}

function PostsLoadingDummy() {
    return (
        <div className="w-full bg-neutral-800 p-4 rounded-lg my-4 shadow-lg">
            <div className="flex">
                <Skeleton variant="circular" width={56} height={56} sx={{ bgcolor: "grey.800" }} />
                <div className="ml-4">
                    <Skeleton variant="text" sx={{ fontSize: "1.5rem", bgcolor: "grey.800" }} width={300} />
                    <Skeleton variant="text" sx={{ fontSize: "1rem", bgcolor: "grey.800" }} width={100} />
                </div>
            </div>
            <div className="py-4 px-2">
                <Skeleton variant="text" sx={{ fontSize: "1rem", bgcolor: "grey.800" }} width={"100%"} />
                <Skeleton variant="text" sx={{ fontSize: "1rem", bgcolor: "grey.800" }} width={"100%"} />
                <Skeleton variant="text" sx={{ fontSize: "1rem", bgcolor: "grey.800" }} width={250} />
            </div>
        </div>
    );
}

function PostsLoadingDummySet() {
    return (
        <>
            <PostsLoadingDummy />
            <PostsLoadingDummy />
            <PostsLoadingDummy />
            <PostsLoadingDummy />
            <PostsLoadingDummy />
        </>
    );
}

function PostContainer() {
    const { postList, loading, getList, getNextList, hasMore } = useApiGetPostList();
    const lastPostRef = useInPageEndFunctionCalling({ loading, hasMore, getNextList });

    useEffect(() => {
        getList();
    }, []);

    return (
        <div className="w-[700px] pt-[7vh]">
            <PostCreate />
            {postList.map((post, index) => {
                if (postList.length === index + 1) {
                    return <Post key={index} post={post} ref={lastPostRef} />;
                } else {
                    return <Post key={index} post={post} />;
                }
            })}
            {loading ? <PostsLoadingDummySet /> : null}
        </div>
    );
}

export default PostContainer;
