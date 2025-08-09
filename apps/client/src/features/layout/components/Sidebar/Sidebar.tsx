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
import { genLorem } from "@/core/lib/etc";
import TxtScroll from "@/common/components/elements/txt/TxtScroll";

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
        className="z__sidebar txt__clr fixed h-full border-l-3 border-w__0 right-0 w-[80vw] sm:w-[500px] md:w-[600px] bg-neutral-950"
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
      >
        <div className="w-full flex h-full flex-col">
          <div className="w-full min-h-[60px] h-[60px] sticky top-0 border-b-3 flex items-center justify-start px-5">
            <TxtScroll
              {...{
                txt: "example@gmail.com",
              }}
            />
          </div>

          <div className="scroll__app overflow-y-auto h-full min-h-0 flex flex-col px-5">
            {genLorem(50)}
          </div>
        </div>
      </motion.div>
    </>
  );
};

export default Sidebar;
