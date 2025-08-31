/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import { FieldValues, FormProvider, UseFormReturn } from "react-hook-form";

type PropsType<T extends FieldValues> = {
  formCtx: UseFormReturn<T>;
  handleSave: () => void;
  testID: string;
} & ChildrenT;

const AuthFormWrap = <T extends FieldValues>({
  formCtx,
  handleSave,
  testID,
  children,
}: PropsType<T>) => {
  return (
    <FormProvider {...formCtx}>
      <form
        data-testid={testID}
        className="w-full grid grid-cols-1"
        onSubmit={handleSave}
      >
        {children}
      </form>
    </FormProvider>
  );
};

export default AuthFormWrap;
