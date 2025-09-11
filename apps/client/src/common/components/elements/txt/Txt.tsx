/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { css, SerializedStyles } from "@emotion/react";
import { SizeT } from "@/common/types/ui";

type PropsType = {
  $size: SizeT;
  $justify: "start" | "center" | "end";
  $ctmCSS?: SerializedStyles;
  txt: string;
};

const Txt: FC<PropsType> = ({ $size, $justify, $ctmCSS, txt }) => {
  return (
    <div
      className="flex"
      css={css`
        justify-content: ${$justify};
      `}
    >
      <span
        className={`txt__${$size}`}
        css={css`
          ${$ctmCSS}
        `}
      >
        {txt}
      </span>
    </div>
  );
};

export default Txt;
