/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { css } from "@emotion/react";
import { TxtSizeT } from "@/common/types/ui";

type PropsType = {
  $size: TxtSizeT;
  $justify: "start" | "center" | "end";
  txt: string;
};

const Txt: FC<PropsType> = ({ $size, $justify, txt }) => {
  return (
    <div
      className="flex"
      css={css`
        justify-content: ${$justify};
      `}
    >
      <span className={`txt__${$size}`}>{txt}</span>
    </div>
  );
};

export default Txt;
