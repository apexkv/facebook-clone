"use client";
import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { usePathname, useRouter } from "next/navigation";
import { motion, AnimatePresence } from "motion/react";
import CloseIcon from "@mui/icons-material/CloseOutlined";
import { closeNotification, emptyNotifications, MessageType } from "@/data/chat_slice";
import { RootState } from "@/data/stores";

function Notification({ msg }: { msg: MessageType }) {
    const dispatch = useDispatch();
    const router = useRouter();
    const anime_time = 10;
    const date = new Date(msg.created_at);
    const formattedDate = `${date.getFullYear()}:${String(date.getMonth() + 1).padStart(2, "0")}:${String(
        date.getDate()
    ).padStart(2, "0")} ${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;

    function closeMsgNotification() {
        dispatch(closeNotification(msg.id));
    }

    function openMsgNotification() {
        console.log("openNotification");
        dispatch(emptyNotifications());
        router.push(`/messenger/${msg.room}`);
    }

    return (
        <motion.div
            exit={{ translateX: "105%", transition: { duration: 1, easings: ["linear"] } }}
            className="relative w-[25vw] py-3 px-4 rounded-md shadow-md my-2 bg-slate-400 overflow-hidden btn-click"
        >
            <div onClick={openMsgNotification} className="flex gap-2 items-center cursor-pointer">
                <h1
                    className="w-10 h-10 flex items-center justify-center text-white font-bold rounded-full"
                    style={{ backgroundColor: `#${"054da8"}` }}
                >
                    {msg.user.full_name.split(" ").map((name: string) => name[0].toUpperCase())}
                </h1>
                <div className="w-[85%] pb-2">
                    <h1 className="w-full overflow-hidden truncate font-bold">{msg.user.full_name}</h1>
                    <p className="w-full overflow-hidden truncate text-sm text-neutral-800">{msg.content}</p>
                    <div className="absolute right-2 bottom-[2px]">
                        <span className="text-xs font-semibold text-neutral-500">{formattedDate.split(" ")[1]}</span>
                    </div>
                </div>
            </div>
            <button
                onClick={closeMsgNotification}
                className="w-6 h-6 absolute right-0 top-0 hover:bg-slate-400 flex items-center justify-center"
            >
                <CloseIcon sx={{ fontSize: 18 }} className="" />
            </button>
            <motion.div
                className="absolute bottom-0 left-0 h-[4px] w-full bg-blue-600 transform origin-left"
                initial={{ scaleX: 1 }}
                animate={{ scaleX: 0, transition: { duration: anime_time } }}
                onAnimationComplete={closeMsgNotification}
            />
        </motion.div>
    );
}

function MsgNotifications() {
    const msg_notifications = useSelector((state: RootState) => state.chat.msg_notifications);
    const pathname = usePathname();
    const [x, setX] = useState<number[]>([1, 2, 3, 4, 5]);

    if (pathname.split("/").length > 2 && pathname.split("/")[1] !== "messenger") {
        return (
            <div className="fixed right-2 top-[7.2vh]">
                <AnimatePresence>
                    {msg_notifications.map((msg) => (
                        <Notification key={msg.id} msg={msg} />
                    ))}
                </AnimatePresence>
            </div>
        );
    }
}

export default MsgNotifications;
