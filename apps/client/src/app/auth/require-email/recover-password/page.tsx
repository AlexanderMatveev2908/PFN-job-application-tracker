/** @jsxImportSource @emotion/react */
"use client";

import RequireEmailForm from "@/features/requireEmail/components/RequireEmailForm/AuthEmailForm";
import { useEmailForm } from "@/features/requireEmail/components/RequireEmailForm/hooks/useEmailForm";
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
      }}
    />
  );
};

export default Page;
