import React from 'react';

function Hr({ my = 2, color = 'bg-white' }: { my?: number; color?: string }) {
	return <div className={`w-full h-[1px] ${color} opacity-10 my-${my}`}></div>;
}

export default Hr;
