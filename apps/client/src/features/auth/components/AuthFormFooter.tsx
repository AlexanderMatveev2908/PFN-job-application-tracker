/** @jsxImportSource @emotion/react */
"use client";

import BtnShim from "@/common/components/buttons/BtnShim/BtnShim";
import BtnsSwapper from "@/common/components/swap/BtnsSwapper";
import {
  PayloadStartSwapT,
  SwapStateT,
} from "@/core/hooks/etc/useSwap/etc/initState";
import { isObjOk } from "@/core/lib/dataStructure";
import type { FC } from "react";
import SpannerLinks from "./SpannerLinks/SpannerLinks";

type PropsType = {
  propsBtnsSwapper: {
    swapState: SwapStateT;
    startSwap: (v: PayloadStartSwapT) => void;
    totSwaps: number;
  };
  isLoading: boolean;
  submitBtnTestID: string;
};

const AuthFormFooter: FC<PropsType> = ({
  propsBtnsSwapper,
  isLoading,
  submitBtnTestID,
}) => {
  return (
    <>
      <div className="w-full grid grid-cols-1 gap-8 p-5">
        {isObjOk(propsBtnsSwapper) && (
          <BtnsSwapper
            {...{
              ...propsBtnsSwapper,
            }}
          />
        )}

        <div className="w-[250px] justify-self-center">
          <BtnShim
            {...{
              type: "submit",
              label: "Submit",
              t_id: submitBtnTestID,
              isLoading,
            }}
          />
        </div>
      </div>
      <SpannerLinks />
    </>
  );
};

export default AuthFormFooter;
