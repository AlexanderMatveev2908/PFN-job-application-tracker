/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { UseFormReturn } from "react-hook-form";
import { EmailFormT } from "./paperwork";
import WrapFormPage from "@/common/components/forms/shapes/WrapFormPage";
import RequireEmailFormBody from "./RequireEmailFormBody";

export type PropsTypeRequireEmailForm = {
  formCtx: UseFormReturn<EmailFormT>;
  handleSave: () => void;
  isLoading: boolean;
  testID: string;
};

const RequireEmailForm: FC<PropsTypeRequireEmailForm> = ({
  formCtx,
  handleSave,
  isLoading,
  testID,
}) => {
  return (
    <WrapFormPage
      {...{
        formCtx,
        handleSave,
        formTestID: testID,
        isLoading,
      }}
    >
      <RequireEmailFormBody
        {...{
          formCtx,
        }}
      />
    </WrapFormPage>
  );
};

export default RequireEmailForm;
