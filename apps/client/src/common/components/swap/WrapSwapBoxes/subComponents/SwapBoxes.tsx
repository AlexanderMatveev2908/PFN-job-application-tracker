/** @jsxImportSource @emotion/react */
"use client";

import { CheckChoiceT } from "@/common/types/ui";
import { css } from "@emotion/react";
import { FieldValues, Path } from "react-hook-form";

type PropsType<T extends FieldValues> = {
  choices: CheckChoiceT[];
  colsForSwap: number;
  isCurr: boolean;
  ids: string[];
  handleClick: (v: T[Path<T>]) => void;
  isCurrChoice: (v: T[Path<T>]) => boolean;
};

const SwapBoxes = <T extends FieldValues>({
  choices,
  colsForSwap,
  isCurr,
  ids,
  handleClick,
  isCurrChoice,
}: PropsType<T>) => {
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
      {choices.map((ch, idx) => {
        const isChosen = isCurrChoice(ch.val as T[Path<T>]);

        return (
          <button
            data-testid={`swap_boxes__${ch.val}`}
            type="button"
            key={ids[idx]}
            className="w-[250px] rounded-xl py-3 flex justify-center items-center h-fit"
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
            onClick={handleClick.bind(null, ch.val as T[Path<T>])}
          >
            <span className="txt__lg text-center">{ch.label}</span>
          </button>
        );
      })}
    </div>
  );
};

export default SwapBoxes;
