/** @jsxImportSource @emotion/react */
"use client";

import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import WrapFormBody from "@/common/components/forms/shapes/subComponents/WrapFormBody";
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
    <WrapFormBody>
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
    </WrapFormBody>
  );
};

export default BodyFormLogin;
