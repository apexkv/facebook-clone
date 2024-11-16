import { ListResponseType } from '@/types/types';
import { AxiosInstance } from 'axios';
import { useCallback, useEffect, useRef, useState } from 'react';

type ApiGetListType = {
	url: string;
	apiClient: AxiosInstance;
};

export function useApiGetList<T>(data: ApiGetListType) {
	const [list, setList] = useState<T[]>([]);
	const [nextLink, setNextLink] = useState<string | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);

	async function getList(link: string | null = data.url) {
		if (!link) return;
		setLoading(true);
		setError(null);
		try {
			const res = await data.apiClient.get(link);
			const responseData = res.data as ListResponseType<T>;
			setList((prevList) => [...prevList, ...responseData.results]);
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

	return { list, loading, error, hasMore, getList, getNextList };
}

type InPageEndFunctionCallingType = {
	loading: boolean;
	hasMore: boolean;
	getNextList: () => void;
};

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
