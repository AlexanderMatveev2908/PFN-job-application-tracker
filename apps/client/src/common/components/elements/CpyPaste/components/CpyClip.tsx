/** @jsxImportSource @emotion/react */
"use client";

import { useEffect, type FC } from "react";
import { easeInOut, motion, useAnimationControls } from "framer-motion";
import Portal from "../../Portal";
import { CoordsTooltipT } from "@/core/hooks/ui/useSyncPortal";
import { css } from "@emotion/react";

type PropsType = {
  isCopied: boolean;
  x: number;
  coords: CoordsTooltipT;
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

const CpyClip: FC<PropsType> = ({ isCopied, x, coords }) => {
  const controls = useAnimationControls();

  useEffect(() => {
    let cancelled = false;

    const run = async () => {
      if (!isCopied) {
        await controls.start("hidden");
        return;
      }

      controls.stop();
      controls.set("hidden");

      await new Promise(requestAnimationFrame);
      if (cancelled) return;

      await controls.start("visible");
    };

    void run();

    return () => {
      cancelled = true;
    };
  }, [x, isCopied, controls]);

  return (
    <Portal>
      <motion.div
        css={css`
          left: calc(${coords.left}px + 50%);
          top: ${coords.top}px;
        `}
        initial="hidden"
        animate={controls}
        variants={variants}
        className="absolute w-[300px] py-2 px-4 border-2 border-neutral-600 rounded-xl flex justify-center items-center pointer-events-none z-60 bg-neutral-950 -translate-x-full"
      >
        <span className="txt__sm">Copied to clipboard</span>
      </motion.div>
    </Portal>
  );
};

export default CpyClip;
