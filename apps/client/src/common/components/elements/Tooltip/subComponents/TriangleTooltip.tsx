/** @jsxImportSource @emotion/react */
"use client";

import { css, SerializedStyles } from "@emotion/react";
import type { FC } from "react";

type PropsType = {
  $clr: string;
  $trgCtmCSS?: SerializedStyles;
};

const TriangleTooltip: FC<PropsType> = ({ $clr, $trgCtmCSS }) => {
  return (
    <div
      className="w-[35px] h-[35px] absolute top-full overflow-hidden"
      css={css`
        ${$trgCtmCSS ??
        `
            right:15%;
          `}
      `}
    >
      <div
        css={css`
          border: 2px solid ${$clr};
        `}
        className="absolute w-[35px] h-[35px] rotate-45 bg-neutral-950 translate-y-[-50%] -top-[6px]"
      ></div>
    </div>
  );
};

export default TriangleTooltip;
