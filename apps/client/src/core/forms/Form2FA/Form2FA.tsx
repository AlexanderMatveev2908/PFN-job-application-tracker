/** @jsxImportSource @emotion/react */
"use client";

import WrapMultiFormSwapper from "@/common/components/swap/WrapMultiFormSwapper/WrapMultiFormSwapper";
import { useListenHeight } from "@/core/hooks/etc/height/useListenHeight";
import { useSwap } from "@/core/hooks/etc/useSwap/useSwap";
import type { FC } from "react";
import TotpForm from "./components/TotpForm/TotpForm";
import BackupCodeForm from "./components/BackupCodeForm/BackupCodeForm";

const Form2FA: FC = () => {
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
      <TotpForm
        {...{
          contentRef,
          isCurr: !currSwap,
        }}
      />

      <BackupCodeForm
        {...{
          contentRef,
          isCurr: !!currSwap,
        }}
      />
    </WrapMultiFormSwapper>
  );
};

export default Form2FA;
