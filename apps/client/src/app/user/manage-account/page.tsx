/** @jsxImportSource @emotion/react */
"use client";

import WrapPage from "@/common/components/HOC/pageWrappers/WrapPage";
import { TokenT } from "@/common/types/tokens";
import { useCheckTypeCbcHmac } from "@/core/hooks/etc/tokens/useCheckTypeCbcHmac";
import type { FC } from "react";

const Page: FC = () => {
  useCheckTypeCbcHmac({
    tokenType: TokenT.MANAGE_ACC,
    pathPush: "/user/access-manage-account",
  });

  return (
    <WrapPage>
      <div className=""></div>
    </WrapPage>
  );
};

export default Page;
