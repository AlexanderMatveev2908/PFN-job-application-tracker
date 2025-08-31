"use client";

import { logFormErrs } from "@/core/lib/etc";
import { __cg } from "@/core/lib/log";
import AuthEmailForm from "@/features/auth/components/AuthEmailForm/AuthEmailForm";
import { useEmailForm } from "@/features/auth/components/AuthEmailForm/hooks/useEmailForm";
import type { FC } from "react";

const Page: FC = () => {
  const { formCtx } = useEmailForm();
  const { handleSubmit } = formCtx;

  const handleSave = handleSubmit(async (data) => {
    __cg(data);
  }, logFormErrs);

  return (
    <AuthEmailForm
      {...{
        formCtx,
        testID: "conf_email",
        isLoading: false,
        handleSave,
      }}
    />
  );
};

export default Page;
