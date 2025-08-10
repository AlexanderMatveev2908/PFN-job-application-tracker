/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import type { FC, RefObject } from "react";

type PropsType = {
  isCurr: boolean;
  contentRef: RefObject<HTMLDivElement | null>;
} & ChildrenT;

const WrapSwap: FC<PropsType> = ({ children, isCurr, contentRef }) => {
  return (
    <div
      ref={isCurr ? contentRef : null}
      className={`grid grid-cols-1 gap-6 w-full h-fit items-start transition-all duration-300 ${
        isCurr ? "opacity-100" : "opacity-0"
      }`}
    >
      {children}
    </div>
  );
};

export default WrapSwap;
