/** @jsxImportSource @emotion/react */
"use client";

import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { logFormErrs } from "@/core/lib/etc";
import { __cg } from "@/core/lib/log";
import RequireEmailForm from "@/features/requireEmail/components/RequireEmailForm/AuthEmailForm";
import { useEmailForm } from "@/features/requireEmail/components/RequireEmailForm/hooks/useEmailForm";
import type { FC } from "react";

const Page: FC = () => {
  const { formCtx } = useEmailForm();
  const { handleSubmit, reset } = formCtx;

  const { wrapAPI, setNotice, nav } = useKitHooks();

  const handleSave = handleSubmit(async (data) => {
    __cg(data);
  }, logFormErrs);

  return (
    <RequireEmailForm
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
