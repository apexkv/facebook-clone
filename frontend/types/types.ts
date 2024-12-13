export type UserType = {
	id: string;
	full_name: string;
	is_friend: boolean;
	sent_request: boolean;
	received_request: boolean;
	mutual_friends: number;
	mutual_friends_list: UserType[];
	mutual_friends_name_list: string[];
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
