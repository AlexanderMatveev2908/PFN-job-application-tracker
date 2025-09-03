/** @jsxImportSource @emotion/react */
"use client";

import WrapMultiFormSwapper from "@/common/components/swap/WrapMultiFormSwapper";
import WrapCSR from "@/common/components/HOC/pageWrappers/WrapCSR";
import { TokenT } from "@/common/types/tokens";
import { useListenHeight } from "@/core/hooks/etc/height/useListenHeight";
import { useCheckTypeCbcHmac } from "@/core/hooks/etc/tokens/useCheckTypeCbcHmac";
import { useSwap } from "@/core/hooks/etc/useSwap/useSwap";
import type { FC } from "react";
import ChangeEmailForm from "@/features/user/pages/manage-account/components/ChangeEmailForm";
import ChangePwdForm from "@/features/user/pages/manage-account/components/ChangePwdForm";
import DelAccountSwap from "@/features/user/pages/manage-account/components/DelAccountSwap";

const Page: FC = () => {
  useCheckTypeCbcHmac({
    tokenType: TokenT.MANAGE_ACC,
    pathPush: "/user/access-manage-account",
  });

  const { startSwap, swapState } = useSwap();
  const { currSwap } = swapState;
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
          },
          propsWrapSwapper: {
            contentH,
          },
          swapState,
          totSwaps: 3,
        }}
      >
        <ChangeEmailForm
          {...{
            contentRef,
            isCurr: currSwap === 0,
            swapState,
          }}
        />

        <ChangePwdForm
          {...{
            contentRef,
            isCurr: currSwap === 1,
            swapState,
          }}
        />

        <DelAccountSwap
          {...{
            contentRef,
            isCurr: currSwap === 2,
            swapState,
          }}
        />
      </WrapMultiFormSwapper>
    </WrapCSR>
  );
};

export default Page;
