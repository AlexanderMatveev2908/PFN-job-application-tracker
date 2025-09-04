/** @jsxImportSource @emotion/react */
"use client";

import WrapMultiFormSwapper from "@/common/components/forms/shapes/swap/WrapMultiFormSwapper/WrapMultiFormSwapper";
import { useListenHeight } from "@/core/hooks/etc/height/useListenHeight";
import { useSwap } from "@/core/hooks/etc/useSwap/useSwap";
import type { FC } from "react";

type PropsType = {};

const Form2FA: FC<PropsType> = ({}) => {
  const { startSwap, swapState } = useSwap();
  const { currSwap } = swapState;

  const { contentRef, contentH } = useListenHeight({
    opdDep: [currSwap],
  });

  return (
    <WrapMultiFormSwapper
      {...{
        formTestID: "2FA",
        propsBtnsSwapper: {
          startSwap,
        },
        propsWrapSwapper: {
          contentH,
        },
        swapState,
        totSwaps: 2,
      }}
    >
      <div className=""></div>
    </WrapMultiFormSwapper>
  );
};

export default Form2FA;
