/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import AuthPageWrap from "../AuthPageWrap";
import AuthFormWrap from "../AuthFormWrap";
import { UseFormReturn } from "react-hook-form";
import { EmailFormT } from "./paperwork";
import AuthFormFooter from "../AuthFormFooter";
import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import { emailField } from "./uiFactory";
import AuthWrapBodyForm from "../AuthWrapBodyForm";

type PropsType = {
  formCtx: UseFormReturn<EmailFormT>;
  handleSave: () => void;
  isLoading: boolean;
  testID: string;
};

const AuthEmailForm: FC<PropsType> = ({
  formCtx,
  handleSave,
  isLoading,
  testID,
}) => {
  return (
    <AuthPageWrap>
      <AuthFormWrap
        {...{
          formCtx,
          handleSave,
          formTestID: testID,
        }}
      >
        <AuthWrapBodyForm>
          <FormFieldTxt
            {...{
              el: emailField,
              control: formCtx.control,
            }}
          />
        </AuthWrapBodyForm>

        <AuthFormFooter
          {...{
            isLoading,
            submitBtnTestID: testID,
          }}
        />
      </AuthFormWrap>
    </AuthPageWrap>
  );
};

export default AuthEmailForm;
