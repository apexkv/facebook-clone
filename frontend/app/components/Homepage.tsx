"use client";
import React, { useEffect } from "react";
import PostContainer from "./PostContainer";
import { getFriendSuggestions } from "@/data/funcs";

function Homepage() {
    useEffect(() => {
        getFriendSuggestions();
    }, []);
    return (
        <div className="w-full flex justify-center">
            <PostContainer />
        </div>
    );
}

export default Homepage;
//jeya
