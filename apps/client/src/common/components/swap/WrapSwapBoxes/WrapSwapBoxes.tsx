/** @jsxImportSource @emotion/react */
"use client";

import { CheckChoiceT, FormFieldCheckT } from "@/common/types/ui";
import { useEffect, useMemo, useState } from "react";
import { FieldValues } from "react-hook-form";
import { getColsForSwap } from "./uiFactory";
import { css } from "@emotion/react";
import SwapBoxes from "./subComponents/SwapBoxes";
import BtnsSwapper from "../components/BtnsSwapper";

type PropsType<T extends FieldValues> = {
  el: FormFieldCheckT<T>;
  choices: CheckChoiceT[];
};

const WrapSwapBoxes = <T extends FieldValues>({
  el,
  choices,
}: PropsType<T>) => {
  const [colsForSwap, setColsForSwap] = useState(getColsForSwap());
  const [currSwap, setCurrSwap] = useState(0);

  useEffect(() => {
    const cb = () => {
      const newColsForSwap = getColsForSwap();
      setColsForSwap(newColsForSwap);

      const maxAllowedSwap =
        Math.ceil(choices.length / (newColsForSwap * 3)) - 1;

      if (currSwap > maxAllowedSwap) setCurrSwap(maxAllowedSwap);
    };
    cb();

    window.addEventListener("resize", cb);

    return () => {
      window.removeEventListener("resize", cb);
    };
  }, [choices.length, currSwap]);

  const totSwaps = useMemo(
    () => Math.ceil(choices.length / (colsForSwap * 3)),
    [choices.length, colsForSwap]
  );

  return (
    <div className="cont__grid__md">
      <div className="w-full flex justify-start">
        <span className="txt__lg">{el.label}</span>
      </div>

      <div className="w-full flex flex-col border-3 border-w__0 rounded-xl max-w-[80%] mx-auto overflow-hidden py-5 gap-10">
        <div
          css={css`
            display: grid;
            grid-template-columns: repeat(${totSwaps}, 100%);
            min-width: 100%;
            transition: 0.6s;
            transform: translateX(-${currSwap * 100}%);
          `}
        >
          {Array.from({ length: totSwaps }).map((_, idx) => {
            const boxesForSwap = colsForSwap * 3;

            return (
              <SwapBoxes
                key={idx}
                {...{
                  choices: choices.slice(
                    idx * boxesForSwap,
                    (idx + 1) * boxesForSwap
                  ),
                  colsForSwap,
                  isCurr: idx === currSwap,
                }}
              />
            );
          })}
        </div>

        <div className="cont__grid__lg p-5">
          <BtnsSwapper
            {...{
              setCurrSwap,
              totSwaps,
              currSwap,
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default WrapSwapBoxes;
