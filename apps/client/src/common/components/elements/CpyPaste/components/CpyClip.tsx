/** @jsxImportSource @emotion/react */
"use client";

import { useEffect, type FC } from "react";
import { easeInOut, motion, useAnimationControls } from "framer-motion";

type PropsType = {
  isCopied: boolean;
  x: number;
};

const variants = {
  hidden: {
    y: "0%",
    opacity: 0,
    transition: { duration: 0.2, ease: easeInOut },
  },
  visible: {
    y: "-150%",
    opacity: 1,
    transition: { duration: 0.3, ease: easeInOut },
  },
};

const CpyClip: FC<PropsType> = ({ isCopied, x }) => {
  const controls = useAnimationControls();

  useEffect(() => {
    if (!isCopied) {
      controls.start("hidden");
      return;
    }

    controls.stop();
    controls.set("hidden");
    requestAnimationFrame(() => {
      controls.start("visible");
    });
  }, [x, isCopied, controls]);

  return (
    <motion.div
      initial="hidden"
      animate={controls}
      variants={variants}
      className="absolute w-[300px] py-2 px-4 h-[40px] border-2 border-neutral-600 top-0 left-1/2 rounded-xl flex justify-center items-center pointer-events-none z-60 bg-neutral-950 -translate-x-1/2 "
    >
      <span className="txt__sm">Copied to clipboard</span>
    </motion.div>
  );
};

export default CpyClip;
