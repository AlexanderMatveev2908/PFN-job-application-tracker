/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import WrapSwapManageAcc from "./subComponents/WrapSwapManageAcc";
import { FormManageAccPropsType } from "../types";

const SwapSetup2FA: FC<Omit<FormManageAccPropsType, "swapState">> = ({
  contentRef,
  isCurr,
}) => {
  const testID = "setup_2FA";

  return (
    <WrapSwapManageAcc
      {...{
        contentRef,
        isCurr,
        title: "Setup 2FA",
        testID,
      }}
    >
      <div className=""></div>
    </WrapSwapManageAcc>
  );
};

export default SwapSetup2FA;
