/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { SwapStateT } from "@/core/hooks/etc/useSwap/etc/initState";
import BtnShadow from "../buttons/BtnShadow";

type PropsType = {
  totSwaps: number;
  swapState: SwapStateT;
  startSwap: (v: number) => void;
};

const BtnsSwapper: FC<PropsType> = ({ swapState, startSwap, totSwaps }) => {
  const { ids } = useGenIDs({ lengths: [2] });

  const { currSwap } = swapState;

  return (
    <div className="w-full grid grid-cols-2">
      {ids[0].map((id, i) => (
        <div
          key={id}
          className={`w-[75px] ${
            !i ? "justify-self-start" : "justify-self-end"
          }`}
        >
          <BtnShadow
            {...{
              act: "NONE",
              el: { Svg: !i ? ChevronLeft : ChevronRight },
              isEnabled: !i ? currSwap >= 1 : currSwap + 1 < totSwaps,
              handleClick: () => {
                const val = !i ? currSwap - 1 : currSwap + 1;
                startSwap(val);
              },
            }}
          />
        </div>
      ))}
    </div>
  );
};

export default BtnsSwapper;
