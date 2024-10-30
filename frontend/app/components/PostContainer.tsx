import React from 'react';
import Post from './Post';
import Hr from './Hr';
import ProfIcon from './ProfIcon';
import { PostType } from '@/data/types';

function PostCreate() {
	return (
		<div className="w-full bg-neutral-800 p-4 rounded-lg mt-4 ">
			<form>
				<div className="flex justify-between">
					<ProfIcon href="/" name="Kavindu" />
					<textarea placeholder="What's on your mind?" className="w-[90%] bg-neutral-700 rounded-[30px] text-lg outline-none px-6 py-4" rows={1}></textarea>
				</div>
				<Hr my={6} />
				<button className="w-full py-2 text-base rounded-full font-medium text-blue-600 hover:bg-blue-600 hover:text-white">Create Post</button>
			</form>
		</div>
	);
}

function PostContainer() {
	const post_list: PostType[] = [
		{
			id: 1,
			user: {
				id: 1,
				name: 'Jackie',
			},
			content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec purus nec nunc tincidunt.',
			likes: 10,
			timeAgo: '2 hours ago',
			isLiked: false,
			comment_list: [
				{
					id: 1,
					user: {
						id: 1,
						name: 'John',
					},
					content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec purus nec nunc tincidunt.',
					likes: 10,
					timeAgo: '2hr',
					isLiked: false,
				},
				{
					id: 2,
					user: {
						id: 1,
						name: 'Mellisa',
					},
					content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec purus nec nunc tincidunt.',
					likes: 8,
					timeAgo: '1hr',
					isLiked: false,
				},
				{
					id: 3,
					user: {
						id: 1,
						name: 'Danna',
					},
					content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec purus nec nunc tincidunt.',
					likes: 3,
					timeAgo: '22m',
					isLiked: false,
				},
			],
		},
		{
			id: 2,
			user: {
				id: 2,
				name: 'Emally',
			},
			content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec purus nec nunc tincidunt.',
			likes: 10,
			timeAgo: '2 hours ago',
			isLiked: false,
			comment_list: [
				{
					id: 1,
					user: {
						id: 1,
						name: 'John',
					},
					content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec purus nec nunc tincidunt.',
					likes: 10,
					timeAgo: '2hr',
					isLiked: false,
				},
				{
					id: 2,
					user: {
						id: 1,
						name: 'Mellisa',
					},
					content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec purus nec nunc tincidunt.',
					likes: 8,
					timeAgo: '1hr',
					isLiked: false,
				},
				{
					id: 3,
					user: {
						id: 1,
						name: 'Danna',
					},
					content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec purus nec nunc tincidunt.',
					likes: 3,
					timeAgo: '22m',
					isLiked: false,
				},
			],
		},
	];
	return (
		<div className="w-[700px]">
			<PostCreate />
			{post_list.map((post) => {
				return <Post key={post.id} post={post} />;
			})}
		</div>
	);
}

export default PostContainer;
