/** @jsxImportSource @emotion/react */
"use client";

import { FieldValues, FormProvider, UseFormReturn } from "react-hook-form";
import { ChildrenT } from "@/common/types/ui";
import SearchBarCtxProvider from "../context/SearchBarCtxProvider";
import PageCounter from "@/features/layout/components/SearchBar/sideComponents/PageCounter/PageCounter";

type PropsType<T extends FieldValues> = {
  formCtx: UseFormReturn<T>;
} & ChildrenT;

const SearchBarWrapper = <T extends FieldValues>({
  formCtx,
  children,
}: PropsType<T>) => {
  return (
    <SearchBarCtxProvider>
      <FormProvider {...formCtx}>
        {children}

        <PageCounter
          {...{
            nHits: 50,
          }}
        />
      </FormProvider>
    </SearchBarCtxProvider>
  );
};

export default SearchBarWrapper;
