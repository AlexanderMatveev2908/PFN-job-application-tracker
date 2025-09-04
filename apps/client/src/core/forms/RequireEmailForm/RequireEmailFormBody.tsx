/** @jsxImportSource @emotion/react */
"use client";

import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import WrapFormBody from "@/common/components/forms/wrappers/subComponents/WrapFormBody";
import type { FC } from "react";
import { UseFormReturn } from "react-hook-form";
import { emailField } from "@/core/uiFactory/formFields";
import { EmailFormT } from "@/core/paperwork";

type PropsType = {
  formCtx: UseFormReturn<EmailFormT>;
};

const RequireEmailFormBody: FC<PropsType> = ({ formCtx }) => {
  return (
    <WrapFormBody>
      <FormFieldTxt
        {...{
          el: emailField,
          control: formCtx.control,
        }}
      />
    </WrapFormBody>
  );
};

export default RequireEmailFormBody;
