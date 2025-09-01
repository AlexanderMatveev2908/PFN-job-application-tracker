/** @jsxImportSource @emotion/react */
"use client";

import { logFormErrs } from "@/core/lib/etc";
import { __cg } from "@/core/lib/log";
import FormResetPwd from "@/core/forms/FormResetPwd/FormResetPwd";
import { usePwdsForm } from "@/core/forms/FormResetPwd/hooks/usePwdsForm";
import { type FC } from "react";
import { useUser } from "@/features/user/hooks/useUser";

const Page: FC = () => {
  const { formCtx } = usePwdsForm();
  const { handleSubmit } = formCtx;

  const handleSave = handleSubmit(async (data) => {
    __cg(data);
  }, logFormErrs);

  const { userState } = useUser();
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
