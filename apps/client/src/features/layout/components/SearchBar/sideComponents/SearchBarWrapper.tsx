/* eslint-disable @typescript-eslint/no-explicit-any */
/** @jsxImportSource @emotion/react */
"use client";

import { FieldValues, FormProvider, UseFormReturn } from "react-hook-form";
import SearchBarCtxProvider from "../context/SearchBarCtxProvider";
import PageCounter from "@/features/layout/components/SearchBar/sideComponents/PageCounter/PageCounter";
import { ReactNode } from "react";

type PropsType<T extends FieldValues, K extends (...args: any) => any[]> = {
  formCtx: UseFormReturn<T>;
  hook: ReturnType<K>;
  children: (arg: { hook: ReturnType<K> }) => ReactNode;
};

const SearchBarWrapper = <
  T extends FieldValues,
  K extends (...args: any) => any[]
>({
  formCtx,
  children,
  hook,
}: PropsType<T, K>) => {
  return (
    <SearchBarCtxProvider>
      <FormProvider {...formCtx}>
        {children({ hook })}

        <PageCounter
          {...{
            nHits: 50,
            hook,
          }}
        />
      </FormProvider>
    </SearchBarCtxProvider>
  );
};

export default SearchBarWrapper;
