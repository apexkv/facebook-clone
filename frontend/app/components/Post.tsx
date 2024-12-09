"use client";
import Link from "next/link";
import React, { useEffect, useState } from "react";
import ThumbUpOutlinedIcon from "@mui/icons-material/ThumbUpOutlined";
import ModeCommentOutlinedIcon from "@mui/icons-material/ModeCommentOutlined";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import SendIcon from "@mui/icons-material/Send";
import { Skeleton } from "@mui/material";
import * as Yup from "yup";
import { commentFormatTime, postFormatTime } from "@/data/funcs";
import { CommentType, PostType } from "@/types/types";
import ProfIcon from "./ProfIcon";
import Hr from "./Hr";
import PopUpPost from "./PopUpPost";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "@/data/stores";
import { apiClientPost } from "@/data/api";
import { Field, Form, Formik, FormikHelpers } from "formik";
import { addCommentToPost, likeOrUnlikeComment, likeOrUnlikePost } from "@/data/post_slice";
import { useApiGetCommentList, useInPageEndFunctionCalling } from "@/data/hooks";

export const commentSchema = Yup.object().shape({
    content: Yup.string().required("Required"),
});

function DummyComment() {
    return (
        <div className="flex flex-row my-2">
            <Skeleton variant="circular" sx={{ bgcolor: "grey.800" }} width={40} height={40} />
            <div className="ml-2 w-3/4 bg-neutral-600 rounded-2xl py-2 px-3">
                <Skeleton variant="text" sx={{ fontSize: "1.5rem", bgcolor: "grey.800" }} width={"40%"} />
                <Skeleton variant="text" sx={{ fontSize: "1rem", bgcolor: "grey.800" }} width={"100%"} />
                <Skeleton variant="text" sx={{ fontSize: "1rem", bgcolor: "grey.800" }} width={"100%"} />
                <Skeleton variant="text" sx={{ fontSize: "1rem", bgcolor: "grey.800" }} width={"60%"} />
            </div>
        </div>
    );
}

export function DummyCommentsList() {
    return (
        <>
            <DummyComment />
            <DummyComment />
            <DummyComment />
        </>
    );
}

export function Comment({
    comment,
    ref,
    postId,
}: {
    comment: CommentType;
    ref?: React.LegacyRef<HTMLDivElement>;
    postId: string;
}) {
    const optionsRef = React.useRef<HTMLDivElement>(null);
    const dispatch = useDispatch();
    const timeAgo = commentFormatTime(comment.created_at);
    const auth = useSelector((state: RootState) => state.auth);
    const post = useSelector((state: RootState) => state.posts);
    const [isOptionOpened, setIsOptionOpened] = useState<boolean>(false);

    async function like_or_unlike() {
        await apiClientPost
            .post(`/comments/${comment.id}/like/`)
            .then((res) => {
                const data = res.data as { count: number; is_liked: boolean };
                console.log(data);
                dispatch(
                    likeOrUnlikeComment({
                        postId: postId,
                        commentId: comment.id,
                        likeCount: data.count,
                        isLiked: data.is_liked,
                    })
                );
            })
            .catch((err) => {
                console.log(err);
            });
    }

    function openOptions() {
        setIsOptionOpened(true);
    }

    function closeOptions(event: MouseEvent) {
        // Check if the click is outside the options menu
        if (optionsRef.current && !optionsRef.current.contains(event.target as Node)) {
            setIsOptionOpened(false);
        }
    }

    useEffect(() => {
        if (isOptionOpened) {
            document.addEventListener("click", closeOptions);
        }
        return () => {
            document.removeEventListener("click", closeOptions);
        };
    }, [isOptionOpened]);

    return (
        <div ref={ref}>
            <div className="my-2 w-fit max-w-[95%] comment-section">
                <div className="flex items-start relative">
                    <div className="flex items-center mr-2">
                        <ProfIcon size={4} userId={comment.user.id} name={comment.user.full_name} />
                    </div>
                    <div>
                        <div className="bg-neutral-600 rounded-2xl py-2 px-3">
                            <Link href={`/profile/${comment.user.id}`} className="flex items-center">
                                <h1 className="font-bold tracking-wide">{comment.user.full_name}</h1>
                            </Link>

                            <p>{comment.content}</p>
                        </div>
                        <div className="flex justify-between mt-1 px-2">
                            <span className="flex gap-4 items-center">
                                <span className="text-neutral-400">{timeAgo}</span>
                                {comment.is_liked ? (
                                    <button onClick={like_or_unlike} className="text-blue-600">
                                        Like
                                    </button>
                                ) : (
                                    <button onClick={like_or_unlike} className="text-neutral-400">
                                        Like
                                    </button>
                                )}
                            </span>
                            <span>
                                {comment.like_count > 0 ? (
                                    <div className="text-neutral-400 text-sm flex gap-2">
                                        {comment.like_count}
                                        <div className="bg-blue-600 w-[20px] h-[20px] rounded-full flex justify-center items-center">
                                            <ThumbUpIcon className="text-white text-xs !w-[14px] !h-[14px]" />
                                        </div>
                                    </div>
                                ) : null}
                            </span>
                        </div>
                    </div>
                    <div className="absolute comment-options-top -right-8" ref={optionsRef}>
                        <button
                            onClick={openOptions}
                            className="comment-options-button flex gap-[3px] hover:bg-neutral-600 rounded-full w-[28px] h-[28px] items-center justify-center"
                        >
                            <div className="w-[3px] h-[3px] rounded-full bg-slate-400" />
                            <div className="w-[3px] h-[3px] rounded-full bg-slate-400" />
                            <div className="w-[3px] h-[3px] rounded-full bg-slate-400" />
                        </button>
                        {isOptionOpened && !post.isCommentOptionsOpen ? (
                            <div className="p-2 bg-neutral-800 rounded-lg shadow-xl flex flex-col text-sm absolute -right-full">
                                <button className="w-48 hover:bg-neutral-600 rounded-lg">Edit</button>
                                <button className="w-48 hover:bg-neutral-600 rounded-lg">Delete</button>
                            </div>
                        ) : null}
                    </div>
                </div>
            </div>
        </div>
    );
}

function CommentsList({ post, isFromFeed }: { post: PostType; isFromFeed: boolean }) {
    const [showPopUpPost, setShowPopUpPost] = useState<boolean>(false);

    function openPopUpPost() {
        setShowPopUpPost(true);
    }

    return (
        <div className="">
            <button className="text-neutral-400 font-semibold" onClick={openPopUpPost}>
                View More
            </button>
            {showPopUpPost ? (
                <PopUpPost post={post} setShowPopUpPost={setShowPopUpPost} isFromFeed={isFromFeed} />
            ) : null}
            <div className="">
                {post.comments.slice(0, 3).map((comment, index) => (
                    <Comment key={index} comment={comment} postId={post.id} />
                ))}
            </div>
        </div>
    );
}

export function CommentsContainer({ post, isFromFeed }: { post: PostType; isFromFeed: boolean }) {
    const dispatch = useDispatch();
    const userData = useSelector((state: RootState) => state.auth);

    const initialValues = { content: "" };

    async function createComment(values: typeof initialValues, formikHelpers: FormikHelpers<typeof initialValues>) {
        await apiClientPost
            .post(`/${post.id}/comments/`, { content: values.content })
            .then((res) => {
                const data = res.data as CommentType;
                dispatch(addCommentToPost({ postId: post.id, comment: data }));
                formikHelpers.resetForm();
            })
            .catch((err) => {
                console.log(err);
            });
    }

    return (
        <div>
            <Hr />
            <CommentsList post={post} isFromFeed={isFromFeed} />
            <Formik
                initialValues={initialValues}
                onSubmit={createComment}
                validationSchema={commentSchema}
                className="mt-4"
            >
                <Form className="flex justify-between items-start">
                    <ProfIcon userId={userData.id} name={userData.full_name} />
                    <Field
                        type="textarea"
                        name="content"
                        className="w-[80%] bg-neutral-700 rounded-[30px] text-lg outline-none px-6 py-4"
                        placeholder={`Comment as ${userData.full_name}`}
                        rows={1}
                    />
                    <button
                        type="submit"
                        className="w-[40px] h-[40px] mt-2 rounded-full flex justify-center items-center bg-blue-600"
                    >
                        <SendIcon className="text-lg" />
                    </button>
                </Form>
            </Formik>
        </div>
    );
}

export function ActionLine({ post, children }: { post: PostType; children: React.ReactNode }) {
    const dispatch = useDispatch();

    async function like_or_unlike() {
        await apiClientPost
            .post(`/${post.id}/like/`)
            .then((res) => {
                const data = res.data as { count: number; is_liked: boolean };
                dispatch(likeOrUnlikePost({ postId: post.id, likeCount: data.count, isLiked: data.is_liked }));
            })
            .catch((err) => {
                console.log(err);
            });
    }

    const [commentSectionOn, setCommentSectionOn] = useState<boolean>(post.comments.length > 0);

    function toggleCommentSection() {
        if (post.comments.length > 0) {
            setCommentSectionOn(true);
        } else {
            setCommentSectionOn(!commentSectionOn);
        }
    }

    return (
        <div>
            <div>
                <div>
                    {post.like_count > 0 ? (
                        <div className="text-neutral-400 text-sm flex gap-2">
                            {post.like_count}
                            <div className="bg-blue-600 w-[20px] h-[20px] rounded-full flex justify-center items-center">
                                <ThumbUpIcon className="text-white text-xs !w-[14px] !h-[14px]" />
                            </div>
                        </div>
                    ) : null}
                </div>
                <Hr />
                <div className="w-full flex gap-1">
                    <div className="w-1/2">
                        {post.is_liked ? (
                            <button
                                onClick={like_or_unlike}
                                className="flex items-center justify-center rounded-md py-2 gap-2 w-full hover:bg-neutral-600"
                            >
                                <ThumbUpIcon className="text-blue-600 cursor-pointer" />
                                <span className="text-blue-600">Like</span>
                            </button>
                        ) : (
                            <button
                                onClick={like_or_unlike}
                                className="flex items-center justify-center rounded-md py-2 gap-2 w-full hover:bg-neutral-600"
                            >
                                <ThumbUpOutlinedIcon className="text-neutral-400 cursor-pointer" />
                                <span>Like</span>
                            </button>
                        )}
                    </div>
                    <div className="w-1/2">
                        <button
                            onClick={toggleCommentSection}
                            className="flex items-center justify-center rounded-md py-2 gap-2 w-full hover:bg-neutral-600"
                        >
                            <ModeCommentOutlinedIcon className="text-neutral-400 cursor-pointer" />
                            <span>Comment</span>
                        </button>
                    </div>
                    {/* <div className="w-1/3">
						<button onClick={like} className="flex items-center justify-center rounded-md py-2 gap-2 w-full hover:bg-neutral-600">
							<ReplyOutlinedIcon className="text-neutral-400 cursor-pointer scale-x-[-1]" />
							<span>Share</span>
						</button>
					</div> */}
                </div>
            </div>
            {commentSectionOn ? children : null}
        </div>
    );
}

function Post({
    post,
    ref,
    isFromFeed = true,
}: {
    post: PostType;
    ref?: React.LegacyRef<HTMLDivElement>;
    isFromFeed?: boolean;
}) {
    return (
        <div className="w-full bg-neutral-800 p-4 rounded-lg my-4 shadow-lg" ref={ref}>
            <div className="flex items-center">
                <ProfIcon userId={post.user.id} name={post.user.full_name} />
                <Link href={`/profile/${post.user.id}`}>
                    <div className="ml-4">
                        <h1 className="font-medium tracking-wide">{post.user.full_name}</h1>
                        <span className="text-neutral-400 text-sm">{postFormatTime(post.created_at)}</span>
                    </div>
                </Link>
            </div>
            <div className="py-4 px-2">
                <p className="text-lg">{post.content}</p>
            </div>
            <ActionLine post={post}>
                <CommentsContainer post={post} isFromFeed={isFromFeed} />
            </ActionLine>
        </div>
    );
}

export default Post;
