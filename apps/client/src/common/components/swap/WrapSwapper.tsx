/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import { css } from "@emotion/react";
import type { FC } from "react";

type PropsType = {
  contentH: number;
  currSwap: number;
  totSwaps: number;
} & ChildrenT;

const WrapSwapper: FC<PropsType> = ({
  children,
  contentH,
  currSwap,
  totSwaps,
}) => {
  return (
    <div
      className="transition-all duration-[0.4s] p-5"
      css={css`
        max-height: ${contentH ? `${contentH}px` : "fit-content"};
        height: ${contentH ? `${contentH}px` : "fit-content"};
        overflow: hidden;
      `}
    >
      <div
        className="w-full h-full flex"
        css={css`
          min-width: ${totSwaps * 100}%;
          transition: 0.4s;
          transform: translateX(-${(100 / totSwaps) * currSwap}%);
        `}
      >
        {children}
      </div>
    </div>
  );
};

export default WrapSwapper;
