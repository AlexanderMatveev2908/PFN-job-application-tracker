/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import WrapFormPage from "@/common/components/forms/shapes/WrapFormPage";
import { UseFormReturn } from "react-hook-form";
import { PwdsFormT } from "../../../features/auth/paperwork";
import WrapFormBody from "@/common/components/forms/shapes/subComponents/WrapFormBody";
import PairPwd from "../../../common/components/HOC/PairPwd/PairPwd";

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
    <WrapFormPage
      {...{
        formCtx,
        handleSave,
        formTestID: testID,
        isLoading,
        appendAuthSpanner: true,
      }}
    >
      <WrapFormBody>
        <PairPwd />
      </WrapFormBody>
    </WrapFormPage>
  );
};

export default FormResetPwd;
