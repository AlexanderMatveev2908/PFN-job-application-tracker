/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { UseFormReturn } from "react-hook-form";
import { EmailFormT } from "./paperwork";
import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import { emailField } from "./uiFactory";
import WrapFormPage from "@/common/components/forms/shapes/WrapFormPage";
import WrapForm from "@/common/components/forms/shapes/WrapForm";
import WrapFormBody from "@/common/components/forms/shapes/WrapFormBody";
import WrapFormFooter from "@/common/components/forms/shapes/WrapFormFooter";

type PropsType = {
  formCtx: UseFormReturn<EmailFormT>;
  handleSave: () => void;
  isLoading: boolean;
  testID: string;
};

const RequireEmailForm: FC<PropsType> = ({
  formCtx,
  handleSave,
  isLoading,
  testID,
}) => {
  return (
    <WrapFormPage>
      <WrapForm
        {...{
          formCtx,
          handleSave,
          formTestID: testID,
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

        <WrapFormFooter
          {...{
            isLoading,
            submitBtnTestID: testID,
          }}
        />
      </WrapForm>
    </WrapFormPage>
  );
};

export default RequireEmailForm;
