/** @jsxImportSource @emotion/react */
"use client";

import { PropsTypeWrapSwap } from "@/common/components/swap/components/WrapSwap";
import WrapSwapMultiForm from "@/common/components/swap/WrapMultiFormSwapper/subComponents/WrapSwapMultiForm";
import { logFormErrs } from "@/core/lib/etc";
import { __cg } from "@/core/lib/log";
import {
  BackupCodeFormT,
  resetValsBackupForm,
  schemaBackupForm,
} from "@/core/paperwork";
import { zodResolver } from "@hookform/resolvers/zod";
import type { FC } from "react";
import { useForm } from "react-hook-form";

type PropsType = {} & Omit<PropsTypeWrapSwap, "children">;

const BackupCodeForm: FC<PropsType> = ({ contentRef, isCurr }) => {
  const formCtx = useForm<BackupCodeFormT>({
    mode: "onChange",
    resolver: zodResolver(schemaBackupForm),
    defaultValues: resetValsBackupForm,
  });

  const { handleSubmit } = formCtx;

  const handleSave = handleSubmit(async (data) => {
    __cg(data);
  }, logFormErrs);

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
