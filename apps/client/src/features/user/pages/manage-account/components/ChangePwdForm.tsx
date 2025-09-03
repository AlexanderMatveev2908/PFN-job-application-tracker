/** @jsxImportSource @emotion/react */
"use client";

import WrapFormManageAcc from "@/features/user/components/WrapFormManageAcc";
import { type FC } from "react";
import { FormManageAccPropsType } from "../types";
import PairPwd from "@/common/components/HOC/PairPwd/PairPwd";
import { useForm } from "react-hook-form";
import { PwdsFormT, pwdsSchema, resetValsPwdsForm } from "@/core/paperwork";
import { zodResolver } from "@hookform/resolvers/zod";
import { __cg } from "@/core/lib/log";
import { logFormErrs } from "@/core/lib/etc";
import { useFocusMultiForm } from "@/core/hooks/etc/focus/useFocusMultiForm";

const ChangePwdForm: FC<FormManageAccPropsType> = ({
  contentRef,
  isCurr,
  swapState,
}) => {
  const formCtx = useForm<PwdsFormT>({
    mode: "onChange",
    resolver: zodResolver(pwdsSchema),
    defaultValues: resetValsPwdsForm,
  });
  const { handleSubmit, setFocus } = formCtx;

  useFocusMultiForm({
    keyField: "password",
    setFocus,
    swapState,
    targetSwap: 1,
  });

  const handleSave = handleSubmit(async (data) => {
    __cg(data);
  }, logFormErrs);

  return (
    <WrapFormManageAcc
      {...{
        contentRef,
        isCurr,
        title: "Change Password",
        handleSave,
        formCtx,
        isLoading: false,
      }}
    >
      <PairPwd
        {...{
          isCurrSwap: isCurr,
          swapMode: swapState.swapMode,
        }}
      />
    </WrapFormManageAcc>
  );
};

export default ChangePwdForm;
