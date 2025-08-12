/** @jsxImportSource @emotion/react */
"use client";

import BtnShim from "@/common/components/buttons/BtnShim/BtnShim";
import BtnsSwapper from "@/common/components/HOC/shapes/BtnsSwapper";
import type { FC } from "react";
import {
  PayloadStartSwapT,
  SwapStateT,
} from "@/core/hooks/etc/useSwap/etc/initState";

type PropsType = {
  swapState: SwapStateT;
  startSwap: (v: PayloadStartSwapT) => void;
};

const FooterForm: FC<PropsType> = ({ startSwap, swapState }) => {
  return (
    <div className="w-full grid grid-cols-1 gap-8 p-5">
      <BtnsSwapper
        {...{
          swapState,
          startSwap,
          totSwaps: 2,
        }}
      />

      <div className="w-[250px] justify-self-center">
        <BtnShim
          {...{
            type: "submit",
            label: "Submit",
          }}
        />
      </div>
    </div>
  );
};

export default FooterForm;
