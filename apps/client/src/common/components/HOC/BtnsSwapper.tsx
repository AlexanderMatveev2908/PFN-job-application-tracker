/** @jsxImportSource @emotion/react */
"use client";

import type { Dispatch, FC, SetStateAction } from "react";
import WrapShadow from "./buttonWrappers/WrapShadow";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import { ChevronLeft, ChevronRight } from "lucide-react";

type PropsType = {
  currSwap: number;
  setCurrSwap: Dispatch<SetStateAction<number>>;
  totSwaps: number;
};

const BtnsSwapper: FC<PropsType> = ({ currSwap, setCurrSwap, totSwaps }) => {
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
              handleClick: () =>
                setCurrSwap((prev: number) => (!i ? prev - 1 : prev + 1)),
            }}
          />
        </div>
      ))}
    </div>
  );
};

export default BtnsSwapper;
