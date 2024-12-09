import { CommentType, ListResponseType, PostType } from '@/types/types';
import { AxiosInstance } from 'axios';
import { useCallback, useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from './stores';
import { addCommentListToPost, addPostList } from './post_slice';
import { apiClientPost } from './api';
import { createSelector } from "reselect";

type InPageEndFunctionCallingType = {
	loading: boolean;
	hasMore: boolean;
	getNextList: () => void;
};


const selectPosts = (state: RootState) => state.posts.posts;

const selectUserPostList = (userId: string | undefined) =>
  createSelector(selectPosts, (posts) =>
    posts.filter((post) => post.is_feed_post === false && post.user.id === userId)
);

const selectFeedPostList = createSelector(selectPosts, (posts) =>
  posts.filter((post) => post.is_feed_post === true)
);

export function useInPageEndFunctionCalling(data: InPageEndFunctionCallingType) {
	const observer = useRef<IntersectionObserver | null>();
	const lastPostRef = useCallback(
		(node: HTMLElement | null) => {
			if (data.loading) return;
			if (observer.current) observer.current.disconnect();
			observer.current = new IntersectionObserver((entries) => {
				if (entries[0].isIntersecting && data.hasMore) {
					data.getNextList();
				}
			});
			if (node) observer.current.observe(node);
		},
		[data.loading, data.hasMore],
	);

	return lastPostRef;
}

export function useApiGetPostList(userId: string|undefined) {
	const dispatch = useDispatch();
	const userPostList = useSelector(selectUserPostList(userId));
  	const feedPostList = useSelector(selectFeedPostList);
	const [nextLink, setNextLink] = useState<string | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);

	const initLink = userId ? `/users/${userId}/posts/` : "/feed/";

	async function getList(link: string | null = initLink) {
		if (!link) return;
		setLoading(true);
		setError(null);
		try {
			const res = await apiClientPost.get(link);
			const responseData = res.data as ListResponseType<PostType>;
			dispatch(addPostList(responseData.results));
			setNextLink(responseData.next);
		} catch (err: any) {
			setError(err.message || 'An error occurred');
			console.error(err);
		} finally {
			setLoading(false);
		}
	}

	async function getNextList() {
		if (loading || !nextLink) return;
		await getList(nextLink);
	}

	const hasMore = Boolean(nextLink);

	return { postList: userId?userPostList:feedPostList , loading, error, hasMore, getList, getNextList };
}


export function useApiGetCommentList(postId: string, isFromFeed: boolean = true) {
	const dispatch = useDispatch();
	const commentList = useSelector((state: RootState) => state.posts.posts).find((post) => post.id === postId)?.comments || [];
	const [nextLink, setNextLink] = useState<string | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);
	const initLink = `${postId}/comments/`

	async function getList(link: string | null = initLink) {
		if (!link) return;
		setLoading(true);
		setError(null);
		try {
			const res = await apiClientPost.get(link);
			const responseData = res.data as ListResponseType<CommentType>;
			console.log(responseData);
			if(initLink === link){
				dispatch(addCommentListToPost({postId:postId, comments:responseData.results.slice(3, responseData.results.length)}));
			}
			dispatch(addCommentListToPost({postId:postId,comments:responseData.results}));
			setNextLink(responseData.next);
		} catch (err: any) {
			setError(err.message || 'An error occurred');
			console.error(err);
		} finally {
			setLoading(false);
		}
	}

	async function getNextList() {
		if (loading || !nextLink) return;
		await getList(nextLink);
	}

	const hasMore = Boolean(nextLink);

	return { commentList, loading, error, hasMore, getList, getNextList };
}