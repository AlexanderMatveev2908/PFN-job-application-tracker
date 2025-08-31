/** @jsxImportSource @emotion/react */
"use client";

import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import AuthWrapBodyForm from "@/features/auth/components/AuthWrapBodyForm";
import type { FC } from "react";
import { mailField, pwdField } from "../uiFactory";
import { useFormContext } from "react-hook-form";
import { LoginFormT } from "../paperwork";
import { useTogglePwd } from "@/core/hooks/etc/useTogglePwd";
import FormFieldPwd from "@/common/components/forms/inputs/FormFieldPwd";

const BodyFormLogin: FC = () => {
  const { control } = useFormContext<LoginFormT>();

  const { handlePwdClick, isPwdShw } = useTogglePwd();

  return (
    <AuthWrapBodyForm>
      <FormFieldTxt
        {...{
          el: mailField,
          control,
        }}
      />

      <FormFieldPwd
        {...{
          el: pwdField,
          control,
          isPwdShw: isPwdShw,
          handleSvgClick: handlePwdClick,
        }}
      />
    </AuthWrapBodyForm>
  );
};

export default BodyFormLogin;
