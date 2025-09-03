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
import SwapSetup2FA from "@/features/user/pages/manage-account/components/SwapSetup2FA";
import { useGetUserState } from "@/features/user/hooks/useGetUserState";

const Page: FC = () => {
  useCheckTypeCbcHmac({
    tokenType: TokenT.MANAGE_ACC,
    pathPush: "/user/access-manage-account",
  });

  const { startSwap, swapState } = useSwap();
  const { currSwap } = swapState;
  const { user, isUsOk, touchedServer } = useGetUserState();
  const { contentRef, contentH } = useListenHeight({
    opdDep: [currSwap, isUsOk],
  });

  const showSetup2FA = user?.is_verified && !user?.use_2FA;

  return (
    <WrapCSR
      {...{
        isApiOk: isUsOk,
        isLoading: !touchedServer,
      }}
    >
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
          totSwaps: showSetup2FA ? 4 : 3,
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

        {showSetup2FA && (
          <SwapSetup2FA
            {...{
              contentRef,
              isCurr: currSwap === 2,
            }}
          />
        )}

        <DelAccountSwap
          {...{
            contentRef,
            isCurr: currSwap === (showSetup2FA ? 3 : 2),
          }}
        />
      </WrapMultiFormSwapper>
    </WrapCSR>
  );
};

export default Page;
