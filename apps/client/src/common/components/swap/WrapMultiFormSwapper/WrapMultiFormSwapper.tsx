/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { ChildrenT } from "@/common/types/ui";
import {
  PayloadStartSwapT,
  SwapStateT,
} from "@/core/hooks/etc/useSwap/etc/initState";
import WrapSwapper from "../WrapSwapper";
import WrapFormFooter from "../../forms/wrappers/subComponents/WrapFormFooter";
import WrapCSR from "../../wrappers/pages/WrapCSR";

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
  propsWrapCSR?: {
    isApiOk?: boolean;
    isLoading?: boolean;
  };
} & ChildrenT;

const WrapMultiFormSwapper: FC<PropsType> = ({
  children,
  formTestID,
  propsBtnsSwapper,
  propsWrapSwapper,
  totSwaps,
  swapState,
  propsWrapCSR = { isApiOk: true, isLoading: false },
}) => {
  return (
    <WrapCSR
      {...{
        isApiOk: propsWrapCSR.isApiOk,
        isLoading: propsWrapCSR.isLoading,
      }}
    >
      <div data-testid={formTestID + "__form"} className="form__shape">
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
    </WrapCSR>
  );
};

export default WrapMultiFormSwapper;
