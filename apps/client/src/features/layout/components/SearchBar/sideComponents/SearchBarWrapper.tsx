/* eslint-disable @typescript-eslint/no-explicit-any */
/** @jsxImportSource @emotion/react */
"use client";

import { FieldValues, FormProvider, UseFormReturn } from "react-hook-form";
import SearchBarCtxProvider from "../context/SearchBarCtxProvider";
import PageCounter from "@/features/layout/components/SearchBar/sideComponents/PageCounter/PageCounter";
import { ReactNode } from "react";
import { ZodObject } from "zod";

type PropsType<T extends FieldValues, K extends any[]> = {
  formCtx: UseFormReturn<T>;
  hook: K;
  schema: ZodObject;
  children: (arg: { hook: K; schema: ZodObject }) => ReactNode;
};

const SearchBarWrapper = <T extends FieldValues, K extends any[]>({
  formCtx,
  children,
  hook,
  schema,
}: PropsType<T, K>) => {
  return (
    <SearchBarCtxProvider>
      <FormProvider {...formCtx}>
        {children({ hook, schema })}

        <PageCounter<T, K>
          {...{
            hook,
          }}
        />
      </FormProvider>
    </SearchBarCtxProvider>
  );
};

export default SearchBarWrapper;
