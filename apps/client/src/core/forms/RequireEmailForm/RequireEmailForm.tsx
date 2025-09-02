/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { UseFormReturn } from "react-hook-form";
import { EmailFormT } from "./paperwork";
import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import { emailField } from "./uiFactory";
import WrapFormPage from "@/common/components/forms/shapes/WrapFormPage";
import WrapFormBody from "@/common/components/forms/shapes/subComponents/WrapFormBody";

type PropsType = {
  formCtx: UseFormReturn<EmailFormT>;
  handleSave: () => void;
  isLoading: boolean;
  testID: string;
  appendAuthSpanner?: boolean;
};

const RequireEmailForm: FC<PropsType> = ({
  formCtx,
  handleSave,
  isLoading,
  testID,
  appendAuthSpanner,
}) => {
  return (
    <WrapFormPage
      {...{
        formCtx,
        handleSave,
        formTestID: testID,
        isLoading,
        appendAuthSpanner,
      }}
    >
      <WrapFormBody>
        <FormFieldTxt
          {...{
            el: emailField,
            control: formCtx.control,
          }}
        />
      </WrapFormBody>
    </WrapFormPage>
  );
};

export default RequireEmailForm;
