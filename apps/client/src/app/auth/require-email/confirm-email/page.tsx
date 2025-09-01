"use client";

import RequireEmailForm from "@/features/requireEmail/components/RequireEmailForm/AuthEmailForm";
import { useEmailForm } from "@/features/requireEmail/components/RequireEmailForm/hooks/useEmailForm";
import type { FC } from "react";

const Page: FC = () => {
  const { formCtx, handleSaveMaker, isLoading } = useEmailForm();

  const handleSave = handleSaveMaker({
    endpointT: "confirm-email",
    msgNotice: "to confirm the account",
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
