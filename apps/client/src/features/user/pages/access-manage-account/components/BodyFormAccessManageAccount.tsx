/** @jsxImportSource @emotion/react */
"use client";

import FormFieldPwd from "@/common/components/forms/inputs/FormFieldPwd";
import WrapFormBody from "@/common/components/forms/wrappers/subComponents/WrapFormBody";
import type { FC } from "react";
import { pwdField } from "../uiFactory";
import { useTogglePwd } from "@/core/hooks/etc/useTogglePwd";
import { useFormContext } from "react-hook-form";
import { PwdFormT } from "@/core/paperwork";

const BodyFormAccessManageAccount: FC = () => {
  const { isPwdShw, handlePwdClick } = useTogglePwd();

  const { control } = useFormContext<PwdFormT>();
  return (
    <WrapFormBody>
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

export default BodyFormAccessManageAccount;
