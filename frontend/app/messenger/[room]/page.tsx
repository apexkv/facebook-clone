"use client";
import { apiClientChat } from "@/data/api";
import { addChatUser, ChatUserType, emptyRoomMessages, MessageType, resetMsgRead } from "@/data/chat_slice";
import { useParams } from "next/navigation";
import React, { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import SendIcon from "@mui/icons-material/SendOutlined";
import SentIcon from "@mui/icons-material/CheckOutlined";
import ReadIcon from "@mui/icons-material/DoneAllOutlined";
import { useInPageEndFunctionCalling } from "@/data/hooks";
import { useWebSocket } from "@/app/components/ChatProvider";
import { RootState } from "@/data/stores";
import { ListResponseType } from "@/types/types";

function MsgTyping({ scrollToBottom }: { scrollToBottom: () => void }) {
    useEffect(() => {
        scrollToBottom();
    }, []);
    return (
        <div className={`w-full flex my-4 justify-start`}>
            <div className={`flex items-start max-w-fit`}>
                <div
                    className={`
                        border-b-[15px] border-b-transparent 
                        border-l-[15px] 
                        border-r-[15px] 
                        border-l-transparent border-r-slate-700
                    `}
                ></div>
                <div className="flex gap-1 px-3 py-4 bg-slate-700 rounded-r-2xl rounded-b-2xl">
                    <div className="w-2 h-2 rounded-full bg-slate-200 b1"></div>
                    <div className="w-2 h-2 rounded-full bg-slate-200 b2"></div>
                    <div className="w-2 h-2 rounded-full bg-slate-200 b3"></div>
                </div>
            </div>
        </div>
    );
}

function Msg({ msg, ref }: { msg: MessageType; ref?: React.LegacyRef<HTMLDivElement> }) {
    const date = new Date(msg.created_at);
    const formattedDate = `${date.getFullYear()}:${String(date.getMonth() + 1).padStart(2, "0")}:${String(
        date.getDate()
    ).padStart(2, "0")} ${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;

    return (
        <div ref={ref} className={`w-full flex my-4 ${msg.direction === "received" ? "justify-start" : "justify-end"}`}>
            <div
                className={`flex items-start max-w-[80%]
                ${msg.direction === "sent" ? "flex-row-reverse" : ""}
                `}
            >
                <div
                    className={`
                        border-b-[15px] border-b-transparent 
                        border-l-[15px] 
                        border-r-[15px] 
                        ${
                            msg.direction === "received"
                                ? "border-l-transparent border-r-slate-700"
                                : "border-r-transparent border-l-blue-600"
                        }
                        `}
                ></div>
                <div
                    className={`w-fit p-2 flex flex-wrap rounded-b-2xl relative ${
                        msg.direction === "received" ? "bg-slate-700 rounded-r-2xl" : "bg-blue-600 rounded-l-2xl"
                    }`}
                >
                    <p>{msg.content}</p>
                    <span className="flex items-center justify-end p-1 gap-2">
                        <span className="text-[10px]">{formattedDate.split(" ")[1]}</span>
                        {msg.direction === "sent" ? (
                            msg.is_read ? (
                                <ReadIcon sx={{ fontSize: 16 }} />
                            ) : (
                                <SentIcon sx={{ fontSize: 16 }} />
                            )
                        ) : null}
                    </span>
                </div>
            </div>
        </div>
    );
}

function LastElement({ lastRef }: { lastRef: React.RefObject<HTMLDivElement> }) {
    useEffect(() => {
        if (lastRef && lastRef.current) {
            lastRef.current.scrollIntoView({ block: "end" });
        }
    }, []);
    return <div ref={lastRef}></div>;
}

function page() {
    const params = useParams<{ room: string }>();
    const dispatch = useDispatch();
    const authUser = useSelector((state: RootState) => state.auth);
    const [isFirstLoad, setIsFirstLoad] = useState(true);
    const { websocket } = useWebSocket();
    const [loading, setLoading] = useState(false);
    const [next, setNext] = useState<string | null>(null);
    const [user, setUser] = useState<ChatUserType | null>(null);
    const [messages, setMessages] = useState<MessageType[]>([]);
    const lastRef = useRef<HTMLDivElement>(null);
    const chatContainerRef = useRef<HTMLDivElement>(null);
    const [typing, setTyping] = useState(false);
    const room = useSelector((state: RootState) => state.chat.chat_users.find((user) => user.id === params.room));
    const onlineRoom = useSelector((state: RootState) =>
        state.chat.online_users.find((user) => user.id === params.room)
    );
    const typingTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
    const [msg, setMsg] = useState("");
    const [pageNo, setPageNo] = useState(0);
    const TYPING_TIMER = 3000;

    function startTyping() {
        setTyping(true);
        if (!typing) {
            websocket?.send(JSON.stringify({ type: "friend.typing.start", data: { room: params.room } }));
        }
    }

    function stopTyping() {
        setTyping(false);
        websocket?.send(JSON.stringify({ type: "friend.typing.stop", data: { room: params.room } }));
    }

    function handleTypingStart(e: React.KeyboardEvent<HTMLTextAreaElement>) {
        if (e.key === "Enter" && !e.shiftKey) {
            if (e.type === "keyup") {
                e.preventDefault();
                sendMessage();
            }
        } else {
            if (!typing) {
                startTyping();
                scrollToBottom();
            }

            if (typingTimeoutRef.current) {
                clearTimeout(typingTimeoutRef.current);
            }

            typingTimeoutRef.current = setTimeout(() => {
                stopTyping();
            }, TYPING_TIMER);
        }
    }

    async function loadUser(link: string | null = `/users/${params.room}/user/`) {
        if (!link) return;
        setLoading(true);
        await apiClientChat
            .get(link)
            .then((res) => {
                const data = res.data as ChatUserType;
                dispatch(addChatUser({ ...data, is_active: true, messages: [], typing: false }));
                setUser(data);
                if (data.unread_count > 0) {
                    markAsMessagesRead();
                }
            })
            .catch((err) => {
                console.log(err);
            })
            .finally(() => {
                setLoading(false);
                loadMessages();
            });
    }

    async function loadMessages(link: string | null = `/messages/${params.room}/`) {
        if (!link) return;
        setLoading(true);
        await apiClientChat
            .get(link)
            .then((res) => {
                const data = res.data as ListResponseType<MessageType>;
                setNext(data.next);
                const pageNum = data.next ? pageNo + 1 : pageNo;
                setPageNo(pageNum);
                let newMessages: MessageType[] = [];
                for (let i = 0; i < data.results.length; i++) {
                    if (!messages.some((msg) => msg.content === data.results[i].content)) {
                        newMessages.unshift(data.results[i]);
                    }
                }
                setMessages((prev) => [...newMessages, ...prev]);
            })
            .catch((err) => {
                console.log(err);
            })
            .finally(() => {
                setLoading(false);
            });
    }

    async function loadNextPage() {
        const container = chatContainerRef.current;
        const previousScrollHeight = container?.scrollHeight || 0;

        await loadMessages(next);

        setTimeout(() => {
            if (container) {
                container.scrollTop = container.scrollHeight - previousScrollHeight;
            }
        }, 0);
    }

    function markAsMessagesRead() {
        if (websocket) {
            websocket.send(
                JSON.stringify({
                    type: "chat.read",
                    data: {
                        room: params.room,
                    },
                })
            );
        }
    }

    function scrollToBottom() {
        setTimeout(() => {
            if (lastRef.current) {
                lastRef.current.scrollIntoView({ block: "end" });
            }
        }, 500);
    }

    const firstRef = useInPageEndFunctionCalling({
        loading: loading,
        hasMore: Boolean(next),
        getNextList: loadNextPage,
    });

    async function sendMessage() {
        if (msg.trim() === "") {
            setMsg("");
            return;
        }
        stopTyping();
        if (typingTimeoutRef.current) {
            clearTimeout(typingTimeoutRef.current);
        }
        setTimeout(() => {
            websocket?.send(
                JSON.stringify({
                    type: "chat.message",
                    data: {
                        room: params.room,
                        user: authUser.id,
                        content: msg.trim(),
                    },
                })
            );
            setMsg("");
        }, 100);
        const randomID = Math.random().toString(36).substring(7);
        setMessages((prevMsg) => [
            ...prevMsg,
            {
                id: randomID,
                content: msg.trim(),
                direction: "sent",
                created_at: new Date().toISOString(),
                user: {
                    id: authUser.id,
                    full_name: authUser.full_name,
                    is_online: true,
                    bg_color: "",
                    created_at: "",
                    is_friend: false,
                    mutual_friends: 0,
                    mutual_friends_list: [],
                    mutual_friends_name_list: [],
                    received_request: false,
                    req_id: "",
                    sent_request: false,
                },
                is_read: false,
                room: params.room,
            },
        ]);
        scrollToBottom();
    }

    useEffect(() => {
        if (messages.length > 0) {
            if (pageNo <= 2) {
                scrollToBottom();
            }
        }
    }, [messages]);

    useEffect(() => {
        if (room?.messages && room.messages.length > 0 && !isFirstLoad) {
            setMessages((prevMsg) => [...prevMsg, ...room.messages]);
            dispatch(emptyRoomMessages(params.room));
            markAsMessagesRead();
        }
    }, [room?.messages]);

    useEffect(() => {
        if (room?.msg_read) {
            setMessages((prevMsg) => prevMsg.map((msg) => ({ ...msg, is_read: true })));
            dispatch(resetMsgRead(params.room));
        }
    }, [room?.msg_read]);

    useEffect(() => {
        loadUser();
        setIsFirstLoad(false);
        markAsMessagesRead();
        dispatch(emptyRoomMessages(params.room));
        setMessages((prevMsg) => prevMsg.map((msg) => ({ ...msg, is_read: true })));
        dispatch(resetMsgRead(params.room));

        setTimeout(() => {
            scrollToBottom();
        }, 800);

        return () => {
            if (typingTimeoutRef.current) {
                clearTimeout(typingTimeoutRef.current);
            }
        };
    }, []);

    return (
        <div className="h-[93vh] w-full">
            <div className="w-full h-[6vh] border-l border-neutral-800 bg-neutral-600 flex items-center px-10">
                <div>
                    <h1 className="text-2xl font-semibold">{user?.friend.full_name}</h1>
                    <p className="text-xs text-green-300 italic h-3">
                        {room?.typing || onlineRoom?.typing ? "typing..." : " "}
                    </p>
                </div>
            </div>
            <div ref={chatContainerRef} className="px-4 h-[75vh] overflow-y-scroll chat-scrollbar">
                {messages.map((msg, index) => {
                    if (index === 0) {
                        return <Msg key={index} msg={msg} ref={firstRef} />;
                    }
                    return <Msg key={index} msg={msg} />;
                })}
                {room?.typing || onlineRoom?.typing ? <MsgTyping scrollToBottom={scrollToBottom} /> : null}
                <LastElement lastRef={lastRef} />
            </div>
            <div className="h-[12vh] w-full py-1.5 px-3 resize-none flex items-start justify-between">
                <textarea
                    rows={3}
                    placeholder={`Chat with ${user?.friend.full_name}`}
                    className="w-[92%] rounded-lg p-2 bg-neutral-600"
                    style={{ resize: "none" }}
                    onKeyDown={handleTypingStart}
                    onKeyUp={handleTypingStart}
                    value={msg}
                    onChange={(e) => setMsg(e.target.value)}
                ></textarea>
                <div className="w-[8%] h-[88px] flex justify-center items-center">
                    <button className="p-4 bg-blue-700 rounded-full">
                        <SendIcon />
                    </button>
                </div>
            </div>
        </div>
    );
}

export default page;
