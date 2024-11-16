'use client';
import Link from 'next/link';
import React, { useState } from 'react';
import ThumbUpOutlinedIcon from '@mui/icons-material/ThumbUpOutlined';
import ModeCommentOutlinedIcon from '@mui/icons-material/ModeCommentOutlined';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import SendIcon from '@mui/icons-material/Send';
import { commentFormatTime, postFormatTime } from '@/data/funcs';
import { CommentType, PostType } from '@/types/types';
import ProfIcon from './ProfIcon';
import Hr from './Hr';
import PopUpPost from './PopUpPost';
import { useSelector } from 'react-redux';
import { RootState } from '@/data/stores';

export function Comment({ comment }: { comment: CommentType }) {
	const [isLiked, setIsLiked] = useState<boolean>(comment.is_liked);
	const timeAgo = commentFormatTime(comment.created_at);
	const [likes, setLikes] = useState<number>(comment.like_count);

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
					<div className="flex items-center mr-2">
						<ProfIcon size={4} userId={comment.user.id} name={comment.user.full_name} />
					</div>
					<div>
						<div className="bg-neutral-600 rounded-2xl py-2 px-3">
							<Link href={`/profile/${comment.user.id}`} className="flex items-center">
								<h1 className="font-bold tracking-wide">{comment.user.full_name}</h1>
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

function CommentsList({ comments, post }: { comments: CommentType[]; post: PostType }) {
	const [showPopUpPost, setShowPopUpPost] = useState<boolean>(false);

	function openPopUpPost() {
		setShowPopUpPost(true);
	}

	return (
		<div className="">
			<button className="text-neutral-400 font-semibold" onClick={openPopUpPost}>
				View More
			</button>
			{showPopUpPost ? <PopUpPost post={post} setShowPopUpPost={setShowPopUpPost} /> : null}
			<div className="">
				{comments.map((comment) => (
					<Comment key={comment.id} comment={comment} />
				))}
			</div>
		</div>
	);
}

export function CommentsContainer({ comments, post }: { comments: CommentType[]; post: PostType }) {
	const userData = useSelector((state: RootState) => state.auth);
	return (
		<div>
			<Hr />
			<CommentsList comments={comments} post={post} />
			<form className="mt-4">
				<div className="flex justify-between items-start">
					<ProfIcon userId={userData.id} name={userData.full_name} />
					<textarea className="w-[80%] bg-neutral-700 rounded-[30px] text-lg outline-none px-6 py-4" placeholder={`Comment as ${userData.full_name}`} rows={1}></textarea>
					<button className="w-[40px] h-[40px] mt-2 rounded-full flex justify-center items-center bg-blue-600">
						<SendIcon className="text-lg" />
					</button>
				</div>
			</form>
		</div>
	);
}

export function ActionLine({ post, children }: { post: PostType; children: React.ReactNode }) {
	const [isLiked, setIsLiked] = useState<boolean>(post.is_liked);
	const [likes, setLikes] = useState<number>(post.like_count);

	function like() {
		setIsLiked(true);
		setLikes(likes + 1);
	}

	function unlike() {
		setIsLiked(false);
		setLikes(likes - 1);
	}

	const [commentSectionOn, setCommentSectionOn] = useState<boolean>(post.comments.length > 0);

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
			{commentSectionOn ? children : null}
		</div>
	);
}

function Post({ post, ref }: { post: PostType; ref?: React.LegacyRef<HTMLDivElement> }) {
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
				<CommentsContainer comments={post.comments} post={post} />
			</ActionLine>
		</div>
	);
}

export default Post;
