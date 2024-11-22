import { CommentType, PostType, TokensType, UserType } from '@/types/types';
import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export type PostListType = {
	posts: PostType[];
    isCommentOptionsOpen: boolean;
};

const initialState: PostListType = {
	posts: [],
    isCommentOptionsOpen: false,
};

export const postSlice = createSlice({
	name: 'posts',
	initialState,
	reducers: {
		addPostList: (state, action: PayloadAction<PostType[]>) => {
            state.posts = [...state.posts, ...action.payload];
        },
        addPost: (state, action: PayloadAction<PostType>) => {
            state.posts = [action.payload, ...state.posts];
        },
        addCommentListToPost: (state, action: PayloadAction<{ postId: string; comments: CommentType[] }>) => {
            const post = state.posts.find((post) => post.id === action.payload.postId);
            if (post) {
                post.comments = [...post.comments, ...action.payload.comments];
            }
        },
        addCommentToPost: (state, action: PayloadAction<{ postId: string; comment: CommentType }>) => {
            const post = state.posts.find((post) => post.id === action.payload.postId);
            if (post) {
                post.comments = [action.payload.comment, ...post.comments];
            }
        },
        likeOrUnlikePost: (state, action: PayloadAction<{ postId: string, isLiked:boolean, likeCount: number }>) => {
            const post = state.posts.find((post) => post.id === action.payload.postId);
            if (post) {
                post.is_liked = action.payload.isLiked;
                post.like_count = action.payload.likeCount;
            }
        },
        likeOrUnlikeComment: (state, action: PayloadAction<{ postId: string; commentId: string, isLiked:boolean, likeCount: number }>) => {
            const post = state.posts.find((post) => post.id === action.payload.postId);
            if (post) {
                const comment = post.comments.find((comment) => comment.id === action.payload.commentId);
                if (comment) {
                    comment.is_liked = action.payload.isLiked;
                    comment.like_count = action.payload.likeCount;
                }
            }
        },
        openCommentOptions: (state) => {
            state.isCommentOptionsOpen = true;
        },
        closeCommentOptions: (state) => {
            state.isCommentOptionsOpen = false;
        },
	},
});

export const { addCommentToPost, addCommentListToPost, addPost, addPostList, likeOrUnlikePost, likeOrUnlikeComment, openCommentOptions, closeCommentOptions } = postSlice.actions;
export default postSlice.reducer;
