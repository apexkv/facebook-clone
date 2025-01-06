"use client";
import React, { useEffect, useState, createContext, useContext } from "react";
import { useDispatch, useSelector } from "react-redux";
import { apiClientChat } from "@/data/api";
import {
    addChatOnlineUser,
    ChatUserType,
    EventType,
    newMessage,
    readAllMessages,
    roomStartTyping,
    roomStopTyping,
} from "@/data/chat_slice";
import { RootState } from "@/data/stores";
import { ListResponseType } from "@/types/types";
import { usePathname } from "next/navigation";

type WebSocketContextType = {
    websocket: WebSocket | null;
    setWebsocket: React.Dispatch<React.SetStateAction<WebSocket | null>>;
};
const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

export const useWebSocket = () => {
    const context = useContext(WebSocketContext);
    if (!context) {
        throw new Error("useWebSocket must be used within a WebSocketProvider");
    }
    return context;
};

function ChatProvider({ children }: { children: React.ReactNode }) {
    const auth = useSelector((state: RootState) => state.auth);
    const dispatch = useDispatch();
    const pathname = usePathname();
    const [websocket, setWebsocket] = useState<WebSocket | null>(null);

    useEffect(() => {
        const ws = new WebSocket(`ws://localhost:888/api/chat/ws/chat/?token=${auth.token.access}`);
        ws.onopen = () => {
            setWebsocket(ws);
        };
        ws.onmessage = (e) => {
            const data = JSON.parse(e.data) as EventType;

            if (data.type === "friend.online" || data.type === "friend.offline") {
                let userData = data.data as ChatUserType;
                dispatch(addChatOnlineUser({ ...userData, is_active: userData.id === pathname.split("/")[2] }));
            } else if (data.type === "chat.message") {
                dispatch(newMessage(data.data));
            } else if (data.type === "friend.typing.start") {
                dispatch(roomStartTyping(data.data.room));
            } else if (data.type === "friend.typing.stop") {
                dispatch(roomStopTyping(data.data.room));
            } else if (data.type === "chat.read") {
                dispatch(readAllMessages(data.data.room));
            }
        };
        ws.onclose = (event) => {
            setWebsocket(null);
        };
        return () => {
            ws.close();
        };
    }, []);
    return <WebSocketContext.Provider value={{ websocket, setWebsocket }}>{children}</WebSocketContext.Provider>;
}

export default ChatProvider;
