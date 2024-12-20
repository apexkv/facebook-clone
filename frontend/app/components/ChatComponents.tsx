"use client";
import React, { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import SendIcon from "@mui/icons-material/Send";
import CloseIcon from "@mui/icons-material/Close";
import MinimizeIcon from "@mui/icons-material/CloseFullscreen";
import { RootState } from "@/data/stores";
import { UserType } from "@/types/types";
import {
    addMessage,
    ChatType,
    closeActiveChat,
    createNewChat,
    MessageType,
    minimizeActiveChat,
    openMinimizedChat,
    toggleActiveChat,
} from "@/data/chat_slice";

function UserLine({ friend }: { friend: UserType }) {
    const randomColor = Math.floor(Math.random() * 16777215).toString(16);
    const dispatch = useDispatch();
    const chats = useSelector((state: RootState) => state.chat.chats);

    function openChat() {
        dispatch(createNewChat({ is_opened: true, messages: [], new_messages: 0, user: friend }));
    }

    return (
        <li
            key={friend.id}
            onClick={openChat}
            className="flex items-center gap-2 px-2 py-2 cursor-pointer hover:bg-neutral-700"
        >
            <h2
                style={{ backgroundColor: `#${randomColor}` }}
                className={`!w-7 !h-7 text-[10px] font-bold flex justify-center items-center rounded-full shadow-md`}
            >
                {friend.full_name
                    .trim()
                    .split(" ")
                    .map((name) => name[0].toUpperCase())}
            </h2>
            <span className="text-[14px]">{friend.full_name}</span>
        </li>
    );
}

function OnlineFriendsList() {
    const [showFriends, setShowFriends] = useState(true);
    const friends = useSelector((state: RootState) => state.chat.users);

    function toggleShowFriends() {
        setShowFriends(!showFriends);
    }

    return (
        <div className="w-[250px] max-h-[400px]">
            <button
                onClick={toggleShowFriends}
                className="px-2 py-1 bg-blue-600 rounded-t-md text-white w-full text-left flex items-center"
            >
                <div className="w-2 h-2 rounded-full bg-green-400" />
                <h3 className="px-2 font-semibold">Online Users ({friends.length})</h3>
            </button>
            {showFriends && (
                <ul className="bg-neutral-600 text-white max-h-[370px] overflow-y-auto">
                    {friends.map((friend) => (
                        <UserLine friend={friend} key={friend.id} />
                    ))}
                </ul>
            )}
        </div>
    );
}

function MinimizedChat({ chat }: { chat: ChatType }) {
    const randomColor = Math.floor(Math.random() * 16777215).toString(16);
    const dispatch = useDispatch();

    function openChat() {
        dispatch(openMinimizedChat(chat.user));
    }

    return (
        <button
            className="relative w-16 h-16 my-1 rounded-full flex items-center justify-center shadow-lg border border-neutral-500"
            style={{ backgroundColor: `#${randomColor}` }}
            onClick={openChat}
        >
            <h1 className="text-white font-bold">
                {chat.user.full_name
                    .trim()
                    .split(" ")
                    .map((name: string) => name[0].toUpperCase())}
            </h1>
            {chat.new_messages > 0 && (
                <span className="w-6 h-6 rounded-full bg-red-500 text-sm text-white flex items-center justify-center absolute top-0 left-0 border">
                    {chat.new_messages}
                </span>
            )}
        </button>
    );
}

function MinimizedChatList() {
    const minimizedChats = useSelector((state: RootState) => state.chat.minimized_chats);
    return (
        <div className="flex flex-col items-end fixed right-1 bottom-[420px]">
            {minimizedChats.map((chat, index) => (
                <MinimizedChat key={index} chat={chat} />
            ))}
        </div>
    );
}

function MsgLine({ msg, ref }: { msg: MessageType; ref?: React.RefObject<HTMLLIElement> }) {
    return (
        <li ref={ref} className={`w-full my-1 flex ${msg.direction === "received" ? "justify-start" : "justify-end"}`}>
            <p
                className={`${
                    msg.direction === "received" ? "bg-blue-500" : "bg-slate-400"
                } text-white text-sm px-2 py-1 rounded-2xl max-w-[85%]`}
            >
                {msg.message}
            </p>
        </li>
    );
}

function OpenedChat({ chat }: { chat: ChatType }) {
    const randomColor = Math.floor(Math.random() * 16777215).toString(16);
    const dispatch = useDispatch();
    const lastMessage = useRef<HTMLLIElement>(null);
    const [newMsq, setNewMsg] = useState("");

    function chatToggele() {
        dispatch(toggleActiveChat(chat.user));
    }

    function sendMsg() {
        if (newMsq.trim() === "") return;
        dispatch(
            addMessage({
                user: chat.user,
                message: { message: newMsq, direction: "sent", user: chat.user, read: true, time: "" },
            })
        );
        setNewMsg("");
    }

    function minChat() {
        dispatch(minimizeActiveChat(chat.user));
    }

    function closeCht() {
        dispatch(closeActiveChat(chat.user));
    }

    useEffect(() => {
        if (lastMessage.current) {
            lastMessage.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [chat.messages]);

    return (
        <div className="w-72 mx-1 text-white shadow-lg border border-neutral-600 border-b-0 rounded-t-lg">
            <div className="px-2 py-1 bg-blue-600 rounded-t-md text-white w-full text-left flex items-center justify-between">
                <button onClick={chatToggele} className="flex w-[80%]">
                    <div
                        className="w-6 h-6 rounded-full text-[12px] font-bold flex items-center justify-center"
                        style={{ backgroundColor: `#${randomColor}` }}
                    >
                        {chat.user.full_name
                            .trim()
                            .split(" ")
                            .map((name: string) => name[0].toUpperCase())}
                    </div>
                    <h3 className="px-2 font-semibold">{chat.user.full_name}</h3>
                </button>
                <button
                    onClick={minChat}
                    className="w-7 h-7 rounded-full hover:bg-blue-400 flex items-center justify-center"
                >
                    <MinimizeIcon sx={{ fontSize: 16 }} />
                </button>
                <button
                    onClick={closeCht}
                    className="w-7 h-7 rounded-full hover:bg-blue-400 flex items-center justify-center"
                >
                    <CloseIcon sx={{ fontSize: 20 }} />
                </button>
            </div>
            {chat.is_opened && (
                <div className="bg-neutral-800 h-[300px]">
                    <ul className="h-[230px] overflow-y-auto chat-scrollbar px-2">
                        {chat.messages.map((msg, index) => {
                            if (chat.messages.length === index + 1) {
                                return <MsgLine msg={msg} key={index} ref={lastMessage} />;
                            }
                            return <MsgLine msg={msg} key={index} />;
                        })}
                    </ul>
                    <div className="flex items-end px-1 py-2 justify-between">
                        <textarea
                            className="w-[85%] bg-neutral-700 rounded-xl px-2 py-1"
                            rows={2}
                            placeholder={`Send to ${chat.user.full_name}`}
                            value={newMsq}
                            onChange={(e) => setNewMsg(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === "Enter") {
                                    sendMsg();
                                }
                            }}
                        ></textarea>
                        <button className="!w-9 !h-9 rounded-full mb-3 bg-blue-500" onClick={sendMsg}>
                            <SendIcon />
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

function OpenedChatList() {
    const openedChatsList = useSelector((state: RootState) => state.chat.active_chats);
    return (
        <div className="flex flex-row-reverse items-end">
            {openedChatsList.map((chat, index) => (
                <OpenedChat key={index} chat={chat} />
            ))}
        </div>
    );
}

function ChatComponents() {
    return (
        <div className="fixed bottom-0 right-2 z-50">
            <MinimizedChatList />
            <div className="flex items-end">
                <OpenedChatList />
                <OnlineFriendsList />
            </div>
        </div>
    );
}

export default ChatComponents;
