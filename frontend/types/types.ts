export type UserType = {
	id: string;
	full_name: string;
};

export type CommentType = {
	id: string;
	user: UserType;
	content: string;
	like_count: number;
	created_at: string;
	is_liked: boolean;
};

export type PostType = {
	id: string;
	user: UserType;
	content: string;
	like_count: number;
	created_at: string;
	is_liked: boolean;
	is_feed_post: boolean;
	comments: CommentType[];
};

export type ListResponseType<T> = {
	count: number;
	next: string | null;
	previous: string | null;
	results: T[];
};

export type TokensType = {
	access: string;
	refresh: string;
};
