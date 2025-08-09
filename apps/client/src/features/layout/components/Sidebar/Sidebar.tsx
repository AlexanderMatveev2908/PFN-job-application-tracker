/** @jsxImportSource @emotion/react */
"use client";

import { useRef, type FC } from "react";
import { css } from "@emotion/react";
import { headerHight } from "@/core/constants/style";
import { useDispatch, useSelector } from "react-redux";
import { getSideState, sideSlice } from "./slice";
import BlackBg from "@/common/components/elements/BlackBg";
import { motion } from "framer-motion";
import { useMouseOut } from "@/core/hooks/ui/useMouseOut";

const Sidebar: FC = () => {
  const sideRef = useRef(null);

  const sideState = useSelector(getSideState);

  const dispatch = useDispatch();

  useMouseOut({
    ref: sideRef,
    cb: () => dispatch(sideSlice.actions.closeSide()),
  });
  return (
    <>
      <BlackBg
        {...{
          classIndexCSS: "z__bg_sidebar",
          isDark: sideState.isOpen,
        }}
      />

      <motion.div
        ref={sideRef}
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
