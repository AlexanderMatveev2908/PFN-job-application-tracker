/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import WrapPage from "../HOC/pageWrappers/WrapPage";
import { ChildrenT } from "@/common/types/ui";
import WrapFormFooter from "../forms/shapes/subComponents/WrapFormFooter";
import WrapSwapper from "./WrapSwapper";
import {
  PayloadStartSwapT,
  SwapStateT,
} from "@/core/hooks/etc/useSwap/etc/initState";

type PropsType = {
  formTestID: string;
  propsBtnsSwapper: {
    startSwap: (v: PayloadStartSwapT) => void;
  };
  propsWrapSwapper: {
    contentH: number;
  };
  totSwaps: number;
  swapState: SwapStateT;
} & ChildrenT;

const WrapMultiFormSwapper: FC<PropsType> = ({
  children,
  formTestID,
  propsBtnsSwapper,
  propsWrapSwapper,
  totSwaps,
  swapState,
}) => {
  return (
    <WrapPage>
      <div data-testid={formTestID + "__form"} className="cont__grid__md">
        <div className="form__shape">
          <WrapSwapper
            {...{
              ...propsWrapSwapper,
              totSwaps,
              currSwap: swapState.currSwap,
            }}
          >
            {children}
          </WrapSwapper>

          <WrapFormFooter
            {...{
              propsBtnsSwapper: {
                ...propsBtnsSwapper,
                swapState,
                totSwaps,
              },
            }}
          />
        </div>
      </div>
    </WrapPage>
  );
};

export default WrapMultiFormSwapper;
