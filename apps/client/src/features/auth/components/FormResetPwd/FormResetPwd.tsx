/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import WrapFormPage from "@/common/components/forms/shapes/WrapFormPage";
import WrapForm from "@/common/components/forms/shapes/WrapForm";
import { UseFormReturn } from "react-hook-form";
import { PwdsFormT } from "../../paperwork";
import WrapFormBody from "@/common/components/forms/shapes/WrapFormBody";
import PairPwd from "../PairPwd/PairPwd";
import WrapFormFooter from "@/common/components/forms/shapes/WrapFormFooter";

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
    <WrapFormPage>
      <WrapForm
        {...{
          formCtx,
          handleSave,
          formTestID: testID,
        }}
      >
        <WrapFormBody>
          <PairPwd />
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

export default FormResetPwd;
