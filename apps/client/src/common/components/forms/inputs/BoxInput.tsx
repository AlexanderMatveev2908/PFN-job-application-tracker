/** @jsxImportSource @emotion/react */
"use client";

import { CheckChoiceT, TestIDT } from "@/common/types/ui";
import { css } from "@emotion/react";
import type { FC } from "react";

type PropsType = {
  handleClick: () => void;
  isChosen: boolean;
  opt: CheckChoiceT;
} & TestIDT;

const BoxInput: FC<PropsType> = ({ testID, isChosen, handleClick, opt }) => {
  return (
    <button
      data-testid={testID}
      type="button"
      className="w-full rounded-xl py-3 px-4 flex justify-center items-center h-fit"
      css={css`
        transition: ${isChosen ? 0.2 : 0.3}s ease-in-out;
        border: 2px solid var(--${isChosen ? "white__0" : "neutral__600"});
        background: var(--${isChosen ? "white__0" : "transparent"});
        transform: scale(${isChosen ? 0.85 : 1});
        cursor: pointer;
        color: var(--${isChosen ? "neutral__950" : "neutral__300"});

        &:hover {
          transform: scale(${isChosen ? 0.85 : 1.15});
        }
      `}
      onClick={handleClick}
    >
      <span className="txt__lg text-center">{opt.label}</span>
    </button>
  );
};

export default BoxInput;
