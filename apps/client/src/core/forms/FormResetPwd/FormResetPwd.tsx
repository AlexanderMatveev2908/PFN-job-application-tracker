/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { UseFormReturn } from "react-hook-form";
import { PwdsFormT } from "../../../features/auth/paperwork";
import WrapFormBody from "@/common/components/forms/shapes/subComponents/WrapFormBody";
import PairPwd from "../../../common/components/HOC/PairPwd/PairPwd";
import WrapAuthFormPage from "@/features/auth/components/WrapAuthFormPage";

type PropsType = {
  formCtx: UseFormReturn<PwdsFormT>;
  handleSave: () => void;
  testID: string;
  isLoading: boolean;
};

const FormResetPwd: FC<PropsType> = ({
  formCtx,
  handleSave,
  testID,
  isLoading,
}) => {
  return (
    <WrapAuthFormPage
      {...{
        formCtx,
        handleSave,
        formTestID: testID,
        isLoading,
      }}
    >
      <WrapFormBody>
        <PairPwd />
      </WrapFormBody>
    </WrapAuthFormPage>
  );
};

export default FormResetPwd;
