/** @jsxImportSource @emotion/react */
"use client";

import BtnShim from "@/common/components/buttons/BtnShim/BtnShim";
import BtnsSwapper from "@/common/components/HOC/BtnsSwapper";
import type { FC } from "react";
import { SwapStateT } from "@/core/hooks/etc/useSwap/etc/initState";
import BtnBbl from "@/common/components/buttons/BtnBbl";

type PropsType = {
  swapState: SwapStateT;
  startSwap: (v: number) => void;
};

const FooterForm: FC<PropsType> = ({ startSwap, swapState }) => {
  return (
    <div className="w-full grid grid-cols-1 gap-14 p-5">
      <BtnsSwapper
        {...{
          swapState,
          startSwap,
          totSwaps: 2,
        }}
      />

      <div className="w-[250px] justify-self-center">
        <BtnBbl
          {...{
            type: "button",
            el: {
              label: "Submit",
            },
            act: "INFO",
          }}
        />
        {/* <BtnShim
          {...{
            type: "submit",
            label: "Submit",
          }}
        /> */}
      </div>
    </div>
  );
};

export default FooterForm;
