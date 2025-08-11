/** @jsxImportSource @emotion/react */
"use client";

import type { Dispatch, FC, SetStateAction } from "react";
import WrapShadow from "./buttonWrappers/WrapShadow";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { SwapModeT } from "@/features/auth/pages/register/Register";

type PropsType = {
  currSwap: number;
  setCurrSwap: Dispatch<SetStateAction<number>>;
  totSwaps: number;
  setSwapMode: Dispatch<SetStateAction<SwapModeT>>;
};

const BtnsSwapper: FC<PropsType> = ({
  currSwap,
  setCurrSwap,
  setSwapMode,
  totSwaps,
}) => {
  const { ids } = useGenIDs({ lengths: [2] });

  return (
    <div className="w-full grid grid-cols-2">
      {ids[0].map((id, i) => (
        <div
          key={id}
          className={`w-[75px] ${
            !i ? "justify-self-start" : "justify-self-end"
          }`}
        >
          <WrapShadow
            {...{
              act: "NONE",
              el: { Svg: !i ? ChevronLeft : ChevronRight },
              wrapper: "html_button",
              isEnabled: !i ? currSwap >= 1 : currSwap + 1 < totSwaps,
              handleClick: () => {
                setSwapMode("swapping");
                setCurrSwap((prev: number) => (!i ? prev - 1 : prev + 1));
              },
            }}
          />
        </div>
      ))}
    </div>
  );
};

export default BtnsSwapper;
