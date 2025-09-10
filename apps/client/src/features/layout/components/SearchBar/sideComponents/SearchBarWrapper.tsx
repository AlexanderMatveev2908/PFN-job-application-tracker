/* eslint-disable @typescript-eslint/no-explicit-any */
/** @jsxImportSource @emotion/react */
"use client";

import { FieldValues, FormProvider, UseFormReturn } from "react-hook-form";
import SearchBarCtxProvider from "../context/SearchBarCtxProvider";
import PageCounter from "@/features/layout/components/SearchBar/sideComponents/PageCounter/PageCounter";
import { ReactNode } from "react";
import { ZodObject } from "zod";

type PropsType<T extends FieldValues, K extends (...args: any) => any[]> = {
  formCtx: UseFormReturn<T>;
  hook: ReturnType<K>;
  schema: ZodObject;
  children: (arg: { hook: ReturnType<K>; schema: ZodObject }) => ReactNode;
};

const SearchBarWrapper = <
  T extends FieldValues,
  K extends (...args: any) => any[]
>({
  formCtx,
  children,
  hook,
  schema,
}: PropsType<T, K>) => {
  return (
    <SearchBarCtxProvider>
      <FormProvider {...formCtx}>
        {children({ hook, schema })}

        <PageCounter
          {...{
            hook,
          }}
        />
      </FormProvider>
    </SearchBarCtxProvider>
  );
};

export default SearchBarWrapper;
