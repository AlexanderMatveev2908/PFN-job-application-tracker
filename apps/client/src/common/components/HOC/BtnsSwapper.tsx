/** @jsxImportSource @emotion/react */
"use client";

import type { Dispatch, FC, SetStateAction } from "react";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa6";
import WrapShadow from "./buttonWrappers/WrapShadow";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";

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
          className={`w-[100px] ${
            !i ? "justify-self-start" : "justify-self-end"
          }`}
        >
          <WrapShadow
            {...{
              act: "NONE",
              el: { Svg: !i ? FaChevronLeft : FaChevronRight },
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
