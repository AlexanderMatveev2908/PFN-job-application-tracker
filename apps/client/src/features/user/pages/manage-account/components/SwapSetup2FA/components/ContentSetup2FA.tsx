/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import BodySwapSetup2FA from "./subComponents/BodySwapSetup2FA";
import FooterSwapSetup2FA from "./subComponents/FooterSwapSetup2FA";
import { FormManageAccPropsType } from "../../../types";
import { Setup2FAReturnT } from "@/features/user/slices/api";

type PropsType = {
  res2FA: Setup2FAReturnT | null;
  handleClick: () => void;
  testID: string;
  isLoading: boolean;
} & FormManageAccPropsType;

const ContentSetup2FA: FC<PropsType> = ({
  isCurr,
  swapState,
  handleClick,
  res2FA,
  isLoading,
  testID,
}) => {
  return (
    <>
      <BodySwapSetup2FA
        {...{
          isCurr,
          res2FA,
          swapMode: swapState.swapMode,
        }}
      />

      <FooterSwapSetup2FA
        {...{
          handleClick,
          res2FA,
          isLoading,
          testID,
        }}
      />
    </>
  );
};

export default ContentSetup2FA;
