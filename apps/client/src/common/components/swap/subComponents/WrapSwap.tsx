/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import type { FC, RefObject } from "react";

export type PropsTypeWrapSwap = {
  isCurr: boolean;
  contentRef: RefObject<HTMLDivElement | null>;
} & ChildrenT;

const WrapSwap: FC<PropsTypeWrapSwap> = ({ children, isCurr, contentRef }) => {
  return (
    <div
      ref={isCurr ? contentRef : null}
      className={`grid grid-cols-1 gap-6 w-full h-fit items-start transition-all duration-300 ${
        isCurr
          ? "opacity-100 pointer-events-auto"
          : "opacity-0 pointer-events-none"
      }`}
    >
      {children}
    </div>
  );
};

export default WrapSwap;
