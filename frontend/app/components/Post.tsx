'use client';
import React, { useState } from 'react';
import Hr from './Hr';
import ProfIcon from './ProfIcon';
import Link from 'next/link';
import ThumbUpOutlinedIcon from '@mui/icons-material/ThumbUpOutlined';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ModeCommentOutlinedIcon from '@mui/icons-material/ModeCommentOutlined';
import ReplyOutlinedIcon from '@mui/icons-material/ReplyOutlined';
import SendIcon from '@mui/icons-material/Send';
import { CommentType, PostType } from '@/data/types';

function Comment({ comment }: { comment: CommentType }) {
	const [isLiked, setIsLiked] = useState<boolean>(comment.isLiked);
	const timeAgo = comment.timeAgo;
	const [likes, setLikes] = useState<number>(comment.likes);

	function like() {
		setIsLiked(true);
		setLikes(likes + 1);
	}

	function unlike() {
		setIsLiked(false);
		setLikes(likes - 1);
	}

	return (
		<div>
			<div className="my-2 w-fit">
				<div className="flex items-start">
					<Link href={`/profile/${comment.user.id}`} className="flex items-center mr-2">
						<ProfIcon size={4} href="/" name={comment.user.name} />
					</Link>
					<div>
						<div className="bg-neutral-600 rounded-2xl py-2 px-3">
							<Link href={`/profile/${comment.user.id}`} className="flex items-center">
								<h1 className="font-bold tracking-wide">{comment.user.name}</h1>
							</Link>

							<p>Lorem ipsum dolor sit amet consectetur adipisicing.</p>
						</div>
						<div className="flex justify-between mt-1 px-2">
							<span className="flex gap-4 items-center">
								<span className="text-neutral-400">{timeAgo}</span>
								{isLiked ? (
									<button onClick={unlike} className="text-blue-600">
										Like
									</button>
								) : (
									<button onClick={like} className="text-neutral-400">
										Like
									</button>
								)}
							</span>
							<span>
								{likes > 0 ? (
									<div className="text-neutral-400 text-sm flex gap-2">
										{likes}
										{likes > 0 ? (
											<div className="bg-blue-600 w-[20px] h-[20px] rounded-full flex justify-center items-center">
												<ThumbUpIcon className="text-white text-xs" />
											</div>
										) : null}
									</div>
								) : null}
							</span>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

function CommentsList({ comments }: { comments: CommentType[] }) {
	return (
		<div className="">
			<button className="text-neutral-400 font-semibold">View More</button>
			<div className="">
				{comments.map((comment) => {
					return <Comment key={comment.id} comment={comment} />;
				})}
			</div>
		</div>
	);
}

function CommentsContainer({ comments }: { comments: CommentType[] }) {
	return (
		<div>
			<Hr />
			<CommentsList comments={comments} />
			<form className="mt-4">
				<div className="flex justify-between items-start">
					<ProfIcon href="/" name="Kavindu" />
					<textarea className="w-[80%] bg-neutral-700 rounded-[30px] text-lg outline-none px-6 py-4" rows={1}></textarea>
					<button className="w-[40px] h-[40px] mt-2 rounded-full flex justify-center items-center bg-blue-600">
						<SendIcon className="text-lg" />
					</button>
				</div>
			</form>
		</div>
	);
}

function ActionLine({ post }: { post: PostType }) {
	const [isLiked, setIsLiked] = useState<boolean>(post.isLiked);
	const [likes, setLikes] = useState<number>(post.likes);

	function like() {
		setIsLiked(true);
		setLikes(likes + 1);
	}

	function unlike() {
		setIsLiked(false);
		setLikes(likes - 1);
	}

	const [commentSectionOn, setCommentSectionOn] = useState<boolean>(post.comment_list.length > 0);

	function toggleCommentSection() {
		setCommentSectionOn(!commentSectionOn);
	}

	return (
		<div>
			<div>
				<div>
					{likes > 0 ? (
						<div className="text-neutral-400 text-sm flex gap-2">
							{likes}
							{likes > 0 ? (
								<div className="bg-blue-600 w-[20px] h-[20px] rounded-full flex justify-center items-center">
									<ThumbUpIcon className="text-white text-xs" />
								</div>
							) : null}
						</div>
					) : null}
				</div>
				<Hr />
				<div className="w-full flex gap-1">
					<div className="w-1/2">
						{isLiked ? (
							<button onClick={unlike} className="flex items-center justify-center rounded-md py-2 gap-2 w-full hover:bg-neutral-600">
								<ThumbUpIcon className="text-blue-600 cursor-pointer" />
								<span className="text-blue-600">Like</span>
							</button>
						) : (
							<button onClick={like} className="flex items-center justify-center rounded-md py-2 gap-2 w-full hover:bg-neutral-600">
								<ThumbUpOutlinedIcon className="text-neutral-400 cursor-pointer" />
								<span>Like</span>
							</button>
						)}
					</div>
					<div className="w-1/2">
						<button onClick={toggleCommentSection} className="flex items-center justify-center rounded-md py-2 gap-2 w-full hover:bg-neutral-600">
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
			{commentSectionOn ? <CommentsContainer comments={post.comment_list} /> : null}
		</div>
	);
}

function Post({ post }: { post: PostType }) {
	return (
		<div className="w-full bg-neutral-800 p-4 rounded-lg my-4 shadow-lg">
			<Link href={`/profile/${post.user.id}`} className="flex items-center">
				<ProfIcon href="/" name={post.user.name} />
				<h1 className="ml-4 font-medium tracking-wide">{post.user.name}</h1>
			</Link>
			<div className="py-4 px-2">
				<p className="text-lg">{post.content}</p>
			</div>
			<ActionLine post={post} />
		</div>
	);
}

export default Post;
