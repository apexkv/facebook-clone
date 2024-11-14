'use client';
import React, { useEffect, useState } from 'react';
import Post from './Post';
import Hr from './Hr';
import ProfIcon from './ProfIcon';
import { PostType, ListResponseType } from '@/types/types';
import axios from 'axios';

const token =
	'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM1NzgwMDY2LCJpYXQiOjE3MzA1OTYwNjYsImp0aSI6IjkxYmFkYzY4ZDEzYTQzZmNhMzFhZGRiNTA2Y2MyNjJmIiwidXNlcl9pZCI6ImM2Y2FiNTU4LWZmZGUtNDVkYy1iNjRhLWJkODM4M2M2M2UzOSJ9.ipdtZh6uSkzCxO-2FLEnBoseXiKqaGBA9oN7iPCyX2Y';

function PostCreate() {
	return (
		<div className="w-full bg-neutral-800 p-4 rounded-lg mt-4 ">
			<form>
				<div className="flex justify-between">
					<ProfIcon userId={'shsfs'} name="Kavindu" />
					<textarea placeholder="What's on your mind?" className="w-[90%] bg-neutral-700 rounded-[30px] text-lg outline-none px-6 py-4" rows={1}></textarea>
				</div>
				<Hr my={4} />
				<button className="w-full py-2 text-base rounded-full font-medium text-blue-600 hover:bg-blue-600 hover:text-white">Create Post</button>
			</form>
		</div>
	);
}

function PostContainer() {
	const [postList, setPostList] = useState<PostType[]>([]);

	async function getPostList(link: string | null = 'http://localhost:8020/api/postwrite/feed/') {
		if (link) {
			await axios
				.get(link, {
					headers: {
						Authorization: token,
					},
				})
				.then((res) => {
					const data: ListResponseType<PostType> = res.data;
					setPostList(data.results);
					console.log(data);
				})
				.catch((err) => {
					console.log(err);
				});
		}
	}

	useEffect(() => {
		getPostList();
	}, []);

	return (
		<div className="w-[700px]">
			<PostCreate />
			{postList.map((post) => {
				return <Post key={post.id} post={post} />;
			})}
		</div>
	);
}

export default PostContainer;
