/** @jsxImportSource @emotion/react */
"use client";

import WrapMultiFormSwapper from "@/common/components/swap/WrapMultiFormSwapper";
import WrapCSR from "@/common/components/HOC/pageWrappers/WrapCSR";
import WrapSwap from "@/common/components/swap/subComponents/WrapSwap";
import WrapSwapper from "@/common/components/swap/WrapSwapper";
import { TokenT } from "@/common/types/tokens";
import { useListenHeight } from "@/core/hooks/etc/height/useListenHeight";
import { useCheckTypeCbcHmac } from "@/core/hooks/etc/tokens/useCheckTypeCbcHmac";
import { useSwap } from "@/core/hooks/etc/useSwap/useSwap";
import { genLorem } from "@/core/lib/etc";
import type { FC } from "react";

const Page: FC = () => {
  useCheckTypeCbcHmac({
    tokenType: TokenT.MANAGE_ACC,
    pathPush: "/user/access-manage-account",
  });

  const { startSwap, swapState } = useSwap();
  const { currSwap, swapMode } = swapState;
  const { contentRef, contentH } = useListenHeight({
    opdDep: [currSwap],
  });

  return (
    <WrapCSR>
      <WrapMultiFormSwapper
        {...{
          formTestID: "manage_acc",
          propsBtnsSwapper: {
            startSwap,
            swapState,
            totSwaps: 2,
          },
        }}
      >
        <WrapSwapper
          {...{
            contentH,
            currSwap,
            totSwaps: 2,
          }}
        >
          <WrapSwap
            {...{
              contentRef,
              isCurr: !currSwap,
            }}
          >
            <div className="">{genLorem(5)}</div>
          </WrapSwap>

          <WrapSwap
            {...{
              contentRef,
              isCurr: currSwap === 1,
            }}
          >
            <div className="">{genLorem(20)}</div>
          </WrapSwap>
        </WrapSwapper>
      </WrapMultiFormSwapper>
    </WrapCSR>
  );
};

export default Page;
