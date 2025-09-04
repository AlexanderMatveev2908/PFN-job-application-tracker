/** @jsxImportSource @emotion/react */
"use client";

import { PropsTypeWrapSwap } from "@/common/components/swap/WrapSwapper/subComponents/WrapSwap";
import WrapSwapMultiForm from "@/common/components/swap/WrapMultiFormSwapper/subComponents/WrapSwapMultiForm";
import { logFormErrs } from "@/core/lib/etc";
import { __cg } from "@/core/lib/log";
import { resetValsTotpForm, schemaTotpCode, ToptFormT } from "@/core/paperwork";
import { zodResolver } from "@hookform/resolvers/zod";
import type { FC } from "react";
import { useForm } from "react-hook-form";

type PropsType = {} & Omit<PropsTypeWrapSwap, "children">;

const TotpForm: FC<PropsType> = ({ contentRef, isCurr }) => {
  const formCtx = useForm<ToptFormT>({
    mode: "onChange",
    resolver: zodResolver(schemaTotpCode),
    defaultValues: resetValsTotpForm,
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
        title: "Totp Code",
      }}
    >
      <div className=""></div>
    </WrapSwapMultiForm>
  );
};

export default TotpForm;
