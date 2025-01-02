"use client";
import { apiClientChat } from "@/data/api";
import { addChatOnlineUserList, addChatUserList, ChatUserType, updateIsActive } from "@/data/chat_slice";
import { useInPageEndFunctionCalling } from "@/data/hooks";
import { RootState } from "@/data/stores";
import { ListResponseType } from "@/types/types";
import Link from "next/link";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import React, { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

function ChatUser({ user, ref }: { user: ChatUserType; ref?: React.LegacyRef<HTMLAnchorElement> }) {
    const chatUserRef = useRef<HTMLDivElement | null>(null);
    const search = useSearchParams();
    const section = search.get("section");

    useEffect(() => {
        if (user.is_active && chatUserRef.current) {
            if (chatUserRef.current.getBoundingClientRect().top < 0) {
                chatUserRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        }
    }, [user.is_active]);
    return (
        <div className="w-full py-1" ref={chatUserRef}>
            <Link
                href={`/messenger/${user.id}${section === "online" ? `?section=${section}` : ""}`}
                className={`flex items-center gap-2 w-full px-4 hover:bg-neutral-600 py-3 rounded-lg ${
                    user.is_active ? "bg-neutral-500" : ""
                }`}
                ref={ref}
            >
                <span
                    className="relative w-10 h-10 rounded-full flex items-center justify-center"
                    style={{ backgroundColor: user.friend.bg_color }}
                >
                    {user.friend.is_online ? (
                        <span className="absolute left-0 top-0 w-3 h-3 rounded-full bg-green-500 border"></span>
                    ) : null}
                    {user.friend.full_name
                        .trim()
                        .split(" ")
                        .map((name: string) => name[0].toUpperCase())}
                </span>
                <div className="w-[70%]">
                    <h1 className={`w-[100%] overflow-hidden truncate ${user.unread_count > 0 ? "font-bold" : ""}`}>
                        {user.friend.full_name}
                    </h1>
                    {user.typing ? (
                        <p className="text-xs text-green-300 italic">typing...</p>
                    ) : user.last_message ? (
                        <p
                            className={`text-xs text-neutral-300 overflow-hidden truncate ${
                                user.unread_count > 0 ? "font-bold" : ""
                            }`}
                        >
                            {user.last_message}
                        </p>
                    ) : null}
                </div>
                {user.unread_count > 0 ? (
                    <span
                        className={`${
                            user.unread_count > 99
                                ? "rounded-3xl p-1"
                                : "w-6 h-6 flex items-center justify-center rounded-full"
                        } bg-red-500 text-[11px]`}
                    >
                        {user.unread_count > 99 ? "99+" : user.unread_count}
                    </span>
                ) : null}
            </Link>
        </div>
    );
}

function ChatUsersList() {
    const urlParams = useSearchParams();
    const section = urlParams.get("section");
    const pathname = usePathname();
    const dispatch = useDispatch();
    const router = useRouter();
    const chatUsers = useSelector((state: RootState) => state.chat.chat_users);
    const chatOnlineUsers = useSelector((state: RootState) => state.chat.online_users);
    const [nextChat, setNextChat] = useState<string | null>(null);
    const [nextChatOnline, setNextChatOnline] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const lastRefChat = useInPageEndFunctionCalling({
        loading: loading,
        hasMore: Boolean(nextChat),
        getNextList: loadNextChatPage,
    });

    const lastRefOnlineChat = useInPageEndFunctionCalling({
        loading: loading,
        hasMore: Boolean(nextChatOnline),
        getNextList: loadNextChatOnlinePage,
    });

    async function loadChatUsers(link: string | null = "/users/") {
        if (!link) return;
        setLoading(true);
        await apiClientChat
            .get(link)
            .then((res) => {
                const data = res.data as ListResponseType<ChatUserType>;
                let users: ChatUserType[] = [];
                for (let i = 0; i < data.results.length; i++) {
                    users.push({
                        ...data.results[i],
                        is_active: data.results[i].id === pathname.split("/")[2],
                        typing: false,
                        messages: [],
                    });
                }
                dispatch(addChatUserList(users));
                setNextChat(data.next);
            })
            .catch((err) => {
                console.log(err);
            })
            .finally(() => {
                setLoading(false);
            });
    }

    async function loadChatOnlineUsers(link: string | null = "/users/?filter=online") {
        if (!link) return;
        setLoading(true);
        await apiClientChat
            .get(link)
            .then((res) => {
                const data = res.data as ListResponseType<ChatUserType>;
                let users: ChatUserType[] = [];
                for (let i = 0; i < data.results.length; i++) {
                    users.push({
                        ...data.results[i],
                        is_active: data.results[i].id === pathname.split("/")[2],
                        typing: false,
                        messages: [],
                    });
                }
                dispatch(addChatOnlineUserList(users));
                setNextChatOnline(data.next);
            })
            .catch((err) => {
                console.log(err);
            })
            .finally(() => {
                setLoading(false);
            });
    }

    async function loadNextChatPage() {
        await loadChatUsers(nextChat);
    }

    async function loadNextChatOnlinePage() {
        await loadChatOnlineUsers(nextChatOnline);
    }

    function toOnline() {
        router.push(`${pathname.split("?")[0]}?section=online`);
    }

    function toChat() {
        router.push(`${pathname.split("?")[0]}`);
    }

    useEffect(() => {
        dispatch(updateIsActive(pathname));
    }, [pathname]);

    useEffect(() => {
        loadChatUsers();
        loadChatOnlineUsers();
    }, []);

    return (
        <div>
            <div className="w-full h-[6vh] pt-4 px-2 bg-neutral-600 flex items-center">
                <button
                    className={`w-1/2 py-2 hover:bg-neutral-500 hover:rounded-lg ${
                        section === "online" ? "" : "rounded-t-lg bg-neutral-900"
                    }`}
                    onClick={toChat}
                >
                    chat
                </button>
                <button
                    className={`w-1/2 py-2 hover:bg-neutral-500 hover:rounded-lg ${
                        section === "online" ? "rounded-t-lg bg-neutral-900" : ""
                    }`}
                    onClick={toOnline}
                >
                    online
                </button>
            </div>
            <div className={`w-[350px] p-2 border-r border-neutral-700 h-[87vh] overflow-y-auto chat-scrollbar`}>
                {section === "online"
                    ? chatOnlineUsers.map((user, index) => {
                          if (chatOnlineUsers.length === index + 1) {
                              return <ChatUser key={index} user={user} ref={lastRefOnlineChat} />;
                          }
                          return <ChatUser key={index} user={user} />;
                      })
                    : chatUsers.map((user, index) => {
                          if (chatUsers.length === index + 1) {
                              return <ChatUser key={index} user={user} ref={lastRefChat} />;
                          }
                          return <ChatUser key={index} user={user} />;
                      })}
            </div>
        </div>
    );
}

function layout({ children }: { children: React.ReactNode }) {
    return (
        <div className="pt-[7vh] flex">
            <ChatUsersList />
            <div style={{ width: "calc(100% - 350px)" }}>{children}</div>
        </div>
    );
}

export default layout;
