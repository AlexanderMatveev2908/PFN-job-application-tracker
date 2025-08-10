/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

type PropsType = {
  currSwap: number;
  idx: number;
} & ChildrenT;

const WrapSwap: FC<PropsType> = ({ currSwap, idx, children }) => {
  return (
    <div
      className={`grid grid-cols-1 gap-6 w-full transition-all duration-300 ${
        currSwap === idx ? "opacity-100" : "opacity-0"
      }`}
    >
      {children}
    </div>
  );
};

export default WrapSwap;
