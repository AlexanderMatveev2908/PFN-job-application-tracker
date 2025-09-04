/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { ChildrenT } from "@/common/types/ui";
import WrapFormFooter from "../../subComponents/WrapFormFooter";
import {
  PayloadStartSwapT,
  SwapStateT,
} from "@/core/hooks/etc/useSwap/etc/initState";
import WrapSwapper from "../WrapSwapper";
import WrapPage from "@/common/components/pageWrappers/WrapPage";

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
    </WrapPage>
  );
};

export default WrapMultiFormSwapper;
