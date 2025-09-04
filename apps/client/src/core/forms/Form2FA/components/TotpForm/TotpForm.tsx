/** @jsxImportSource @emotion/react */
"use client";

import { PropsTypeWrapSwap } from "@/common/components/swap/components/WrapSwap";
import WrapSwapMultiForm from "@/common/components/swap/WrapMultiFormSwapper/subComponents/WrapSwapMultiForm";
import { ToptFormT } from "@/core/paperwork";
import type { FC } from "react";
import { UseFormReturn } from "react-hook-form";

type PropsType = {
  formCtx: UseFormReturn<ToptFormT>;
  handleSave: () => void;
} & Omit<PropsTypeWrapSwap, "children">;

const TotpForm: FC<PropsType> = ({
  contentRef,
  isCurr,
  formCtx,
  handleSave,
}) => {
  return (
    <WrapSwapMultiForm
      {...{
        contentRef,
        isCurr,
        formCtx,
        handleSave,
        isLoading: false,
        title: "Totp Code",
      }}
    >
      <div className=""></div>
    </WrapSwapMultiForm>
  );
};

export default TotpForm;
