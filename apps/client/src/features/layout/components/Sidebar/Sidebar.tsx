/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { css } from "@emotion/react";
import { headerHight } from "@/core/constants/style";
import { useSelector } from "react-redux";
import { getSideState } from "./slice";
import BlackBg from "@/common/components/elements/BlackBg";
import { motion } from "framer-motion";

const Sidebar: FC = () => {
  const sideState = useSelector(getSideState);

  return (
    <>
      <BlackBg
        {...{
          classIndexCSS: "z__bg_sidebar",
          isDark: sideState.isOpen,
        }}
      />

      <motion.div
        className="z__sidebar fixed h-full border-l-3 border-w_0 right-0 w-[80vw] sm:w-[500px] md:w-[600px] bg-neutral-950"
        css={css`
          top: ${headerHight}px;
        `}
        initial={{
          x: "100%",
          opacity: 0,
        }}
        transition={{
          x: { duration: 0.4, ease: "easeInOut" },
          opacity: { duration: 0.3, ease: "linear" },
        }}
        animate={{
          x: sideState.isOpen ? "0" : "100%",
          opacity: sideState.isOpen ? 1 : 0,
        }}
      ></motion.div>
    </>
  );
};

export default Sidebar;
