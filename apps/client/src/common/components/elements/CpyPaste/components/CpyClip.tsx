/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { easeInOut, motion } from "framer-motion";

type PropsType = {
  isCopied: boolean;
};

const CpyClip: FC<PropsType> = ({ isCopied }) => {
  return (
    <motion.div
      initial={{
        y: 0,
        opacity: 0,
      }}
      transition={{
        duration: 0.3,
        ease: easeInOut,
      }}
      animate={{
        y: isCopied ? "-150%" : "0",
        opacity: isCopied ? 1 : 0,
      }}
      className="absolute w-[300px] py-2 px-4 h-[40px] border-2 border-neutral-600 top-0 left-1/2 rounded-xl flex justify-center items-center pointer-events-none z-60 bg-neutral-950 -translate-x-1/2 "
    >
      <span className="txt__sm">Copied to clipboard</span>
    </motion.div>
  );
};

export default CpyClip;
