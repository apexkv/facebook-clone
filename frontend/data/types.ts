export type UserType = {
	id: number;
	name: string;
};

export type CommentType = {
	id: number;
	user: UserType;
	content: string;
	likes: number;
	timeAgo: string;
	isLiked: boolean;
};

export type PostType = {
	id: number;
	user: UserType;
	content: string;
	likes: number;
	timeAgo: string;
	isLiked: boolean;
	comment_list: CommentType[];
};
