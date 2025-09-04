/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import { ChevronLeft, ChevronRight } from "lucide-react";
import {
  PayloadStartSwapT,
  SwapStateT,
} from "@/core/hooks/etc/useSwap/etc/initState";
import BtnShadow from "@/common/components/buttons/BtnShadow";

export type PropsTypeBtnsSwapper = {
  totSwaps: number;
  swapState: SwapStateT;
  startSwap: (v: PayloadStartSwapT) => void;
};

const BtnsSwapper: FC<PropsTypeBtnsSwapper> = ({
  swapState,
  startSwap,
  totSwaps,
}) => {
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
              testID: !i ? "btns_swapper_prev_swap" : "btns_swapper_next_swap",
              act: "NONE",
              el: { Svg: !i ? ChevronLeft : ChevronRight },
              isEnabled: !i ? currSwap >= 1 : currSwap + 1 < totSwaps,
              handleClick: () => {
                const val = !i ? currSwap - 1 : currSwap + 1;
                startSwap({ swap: val });
              },
            }}
          />
        </div>
      ))}
    </div>
  );
};

export default BtnsSwapper;
