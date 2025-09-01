/** @jsxImportSource @emotion/react */
"use client";

import { logFormErrs } from "@/core/lib/etc";
import { __cg } from "@/core/lib/log";
import FormResetPwd from "@/features/auth/components/FormResetPwd/FormResetPwd";
import { usePwdsForm } from "@/features/auth/components/FormResetPwd/hooks/usePwdsForm";
import type { FC } from "react";

const Page: FC = () => {
  const { formCtx } = usePwdsForm();
  const { handleSubmit } = formCtx;

  const handleSave = handleSubmit(async (data) => {
    __cg(data);
  }, logFormErrs);

  return (
    <FormResetPwd
      {...{
        handleSave,
        formCtx,
        testID: "recover_pwd",
        isLoading: false,
      }}
    />
  );
};

export default Page;
