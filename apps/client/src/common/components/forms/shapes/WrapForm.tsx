/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import { FieldValues, FormProvider, UseFormReturn } from "react-hook-form";

type PropsType<T extends FieldValues> = {
  formCtx: UseFormReturn<T>;
  handleSave: () => void;
  formTestID: string;
} & ChildrenT;

const WrapForm = <T extends FieldValues>({
  formCtx,
  handleSave,
  formTestID,
  children,
}: PropsType<T>) => {
  return (
    <FormProvider {...formCtx}>
      <form
        data-testid={formTestID + "__form"}
        className="w-full grid grid-cols-1"
        onSubmit={handleSave}
      >
        {children}
      </form>
    </FormProvider>
  );
};

export default WrapForm;
