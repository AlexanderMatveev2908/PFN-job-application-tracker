/** @jsxImportSource @emotion/react */
"use client";

import { PropsTypeWrapSwap } from "@/common/components/swap/components/WrapSwap";
import WrapSwapMultiForm from "@/common/components/swap/WrapMultiFormSwapper/subComponents/WrapSwapMultiForm";
import { BackupCodeFormT } from "@/core/paperwork";
import type { FC } from "react";
import { UseFormReturn } from "react-hook-form";

type PropsType = {
  formCtx: UseFormReturn<BackupCodeFormT>;
  handleSave: () => void;
} & Omit<PropsTypeWrapSwap, "children">;

const BackupCodeForm: FC<PropsType> = ({
  formCtx,
  handleSave,
  contentRef,
  isCurr,
}) => {
  return (
    <WrapSwapMultiForm
      {...{
        contentRef,
        isCurr,
        formCtx,
        handleSave,
        isLoading: false,
        title: "Backup Code",
      }}
    >
      <div className=""></div>
    </WrapSwapMultiForm>
  );
};

export default BackupCodeForm;
