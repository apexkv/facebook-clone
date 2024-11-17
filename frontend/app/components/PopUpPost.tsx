import { CommentType, PostType } from '@/types/types';
import Link from 'next/link';
import React, { useEffect } from 'react';
import SendIcon from '@mui/icons-material/Send';
import CloseIcon from '@mui/icons-material/CloseSharp';
import { postFormatTime } from '@/data/funcs';
import ProfIcon from './ProfIcon';
import { ActionLine, Comment, DummyCommentsList } from './Post';
import Hr from './Hr';
import { apiClientPost } from '@/data/api';
import { useSelector } from 'react-redux';
import { RootState } from '@/data/stores';
import { useApiGetList, useInPageEndFunctionCalling } from '@/data/hooks';

function PopUpPost({ post, setShowPopUpPost }: { post: PostType; setShowPopUpPost: React.Dispatch<React.SetStateAction<boolean>> }) {
	const userData = useSelector((state: RootState) => state.auth);

	const { list: comments, loading, getList: getPostList, getNextList, hasMore } = useApiGetList<CommentType>({ url: `${post.id}/comments/`, apiClient: apiClientPost });
	const lastPostRef = useInPageEndFunctionCalling({ loading, hasMore, getNextList });

	function closePopUp() {
		// Re-enable posts scrolling when popup is closed
		window.document.body.classList.remove('overflow-hidden');
		setShowPopUpPost(false);
	}

	useEffect(() => {
		getPostList();
		// Prevent posts scrolling when popup is open
		window.document.body.classList.add('overflow-hidden');
		return () => {
			window.document.body.classList.remove('overflow-hidden');
		};
	}, []);

	return (
		<div className="fixed w-screen h-screen top-0 right-0 bottom-0 left-0 flex justify-center items-center z-30">
			<div className="absolute w-screen h-screen top-0 right-0 bottom-0 left-0 bg-neutral-950 opacity-50 z-40" onClick={closePopUp} />
			<div className="w-full bg-neutral-800 p-4 rounded-lg my-4 shadow-lg z-50 max-w-[700px] relative">
				<button className="text-white absolute right-2 top-2 rounded-full bg-neutral-700 p-1" onClick={closePopUp}>
					<CloseIcon />
				</button>
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
					<div>
						<Hr />
						<div className="overflow-y-scroll h-[50vh] comments-scrollbar">
							{comments.map((comment, index) => {
								if (comments.length === index + 1) {
									return <Comment key={comment.id} comment={comment} ref={lastPostRef} />;
								} else {
									return <Comment key={comment.id} comment={comment} />;
								}
							})}
							{loading ? <DummyCommentsList /> : null}
						</div>
						<form className="mt-4">
							<div className="flex justify-between items-start">
								<ProfIcon userId={userData.id} name={userData.full_name} />
								<textarea
									className="w-[80%] bg-neutral-700 rounded-[30px] text-lg outline-none px-6 py-4"
									placeholder={`Comment as ${userData.full_name}`}
									rows={1}
								></textarea>
								<button className="w-[40px] h-[40px] mt-2 rounded-full flex justify-center items-center bg-blue-600">
									<SendIcon className="text-lg" />
								</button>
							</div>
						</form>
					</div>
				</ActionLine>
			</div>
		</div>
	);
}

export default PopUpPost;
