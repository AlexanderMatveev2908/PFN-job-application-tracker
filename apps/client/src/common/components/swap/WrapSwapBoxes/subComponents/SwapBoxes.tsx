/** @jsxImportSource @emotion/react */
"use client";

import { CheckChoiceT } from "@/common/types/ui";
import type { FC } from "react";
import { css } from "@emotion/react";

type PropsType = {
  choices: CheckChoiceT[];
  colsForSwap: number;
  isCurr: boolean;
};

const SwapBoxes: FC<PropsType> = ({ choices, colsForSwap, isCurr }) => {
  return (
    <div
      className="w-full justify-items-center gap-8 h-fit items-start"
      css={css`
        display: grid;
        grid-template-columns: repeat(${colsForSwap}, 1fr);
        transition: 0.3s;
        opacity: ${isCurr ? 1 : 0};
      `}
    >
      {choices.map((ch, idx) => (
        <div key={idx} className="w-[100px] tb">
          {ch.val}
        </div>
      ))}
    </div>
  );
};

export default SwapBoxes;
