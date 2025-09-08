/** @jsxImportSource @emotion/react */
"use client";

import { FieldValues, FormProvider, UseFormReturn } from "react-hook-form";
import SearchBarCtxProvider from "./context/SearchBarCtxProvider";
import { ChildrenT } from "@/common/types/ui";

type PropsType<T extends FieldValues> = {
  formCtx: UseFormReturn<T>;
} & ChildrenT;

const SearchBarWrapper = <T extends FieldValues>({
  formCtx,
  children,
}: PropsType<T>) => {
  return (
    <SearchBarCtxProvider>
      <FormProvider {...formCtx}>{children}</FormProvider>
    </SearchBarCtxProvider>
  );
};

export default SearchBarWrapper;
