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
        y: isCopied ? "-125%" : "0",
        opacity: isCopied ? 1 : 0,
      }}
      className="absolute w-[200px] h-[40px] border-2 border-blue_pmr top-0 right-0 rounded-xl bg-white_sec flex justify-center items-center pointer-events-none"
    >
      <span className="txt__h_xxs text-black_sec">Copied to clipboard</span>
    </motion.div>
  );
};

export default CpyClip;
