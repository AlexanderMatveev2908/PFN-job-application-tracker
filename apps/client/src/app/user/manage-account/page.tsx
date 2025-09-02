/** @jsxImportSource @emotion/react */
"use client";

import WrapMultiForm from "@/common/components/forms/shapes/WrapMultiForm";
import { TokenT } from "@/common/types/tokens";
import { useCheckTypeCbcHmac } from "@/core/hooks/etc/tokens/useCheckTypeCbcHmac";
import { useSwap } from "@/core/hooks/etc/useSwap/useSwap";
import type { FC } from "react";

const Page: FC = () => {
  useCheckTypeCbcHmac({
    tokenType: TokenT.MANAGE_ACC,
    pathPush: "/user/access-manage-account",
  });

  const { startSwap, swapState } = useSwap();

  return (
    <WrapMultiForm
      {...{
        formTestID: "manage_acc",
        propsBtnsSwapper: {
          startSwap,
          swapState,
          totSwaps: 2,
        },
      }}
    >
      <div className=""></div>
    </WrapMultiForm>
  );
};

export default Page;
