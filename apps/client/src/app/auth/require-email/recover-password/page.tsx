/** @jsxImportSource @emotion/react */
"use client";

import RequireEmailForm from "@/core/forms/RequireEmailForm/RequireEmailForm";
import { useEmailForm } from "@/core/forms/RequireEmailForm/hooks/useEmailForm";
import type { FC } from "react";

const Page: FC = () => {
  const { formCtx, handleSaveMaker, isLoading } = useEmailForm();

  const handleSave = handleSaveMaker({
    endpointT: "recover-pwd",
    msgNotice: "to recover the password",
  });

  return (
    <RequireEmailForm
      {...{
        formCtx,
        testID: "conf_email",
        isLoading,
        handleSave,
        appendAuthSpanner: true,
      }}
    />
  );
};

export default Page;
