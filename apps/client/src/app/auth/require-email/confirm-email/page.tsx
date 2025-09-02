"use client";

import RequireAuthEmailForm from "@/features/auth/components/RequireAuthEmailForm";
import { useEmailForm } from "@/core/forms/RequireEmailForm/hooks/useEmailForm";
import type { FC } from "react";

const Page: FC = () => {
  const { formCtx, handleSaveMaker, isLoading } = useEmailForm();

  const handleSave = handleSaveMaker({
    endpointT: "confirm-email",
    msgNotice: "to confirm the account",
  });

  return (
    <RequireAuthEmailForm
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
