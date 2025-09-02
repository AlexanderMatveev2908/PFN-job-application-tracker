/** @jsxImportSource @emotion/react */
"use client";

import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import WrapFormBody from "@/common/components/forms/shapes/subComponents/WrapFormBody";
import type { FC } from "react";
import { emailField } from "./uiFactory";
import { UseFormReturn } from "react-hook-form";
import { EmailFormT } from "./paperwork";

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
