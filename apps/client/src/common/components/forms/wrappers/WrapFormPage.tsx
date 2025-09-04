/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import { isObjOk } from "@/core/lib/dataStructure";
import { FieldValues, FormProvider, UseFormReturn } from "react-hook-form";
import WrapFormFooter from "./subComponents/WrapFormFooter";
import { ReactNode } from "react";
import WrapPage from "../../wrappers/pages/WrapPage";
import { PropsTypeBtnsSwapper } from "../../swap/components/BtnsSwapper";
import ProgressSwap from "../../swap/components/ProgressSwap";

export type WrapFormPagePropsType<T extends FieldValues> = {
  propsProgressSwap?: {
    currSwap: number;
    totSwaps: number;
  };
  propsBtnsSwapper?: PropsTypeBtnsSwapper;
  formCtx: UseFormReturn<T>;
  handleSave: () => void;
  formTestID: string;
  isLoading: boolean;
  appendAuthSpanner?: boolean;
  AdditionalFooterNode?: () => ReactNode;
} & ChildrenT;

const WrapFormPage = <T extends FieldValues>({
  propsProgressSwap,
  children,
  formCtx,
  handleSave,
  formTestID,
  isLoading,
  propsBtnsSwapper,
  AdditionalFooterNode,
}: WrapFormPagePropsType<T>) => {
  return (
    <WrapPage>
      {isObjOk(propsProgressSwap) && (
        <ProgressSwap
          {...({
            maxW: 800,
            ...propsProgressSwap,
          } as WrapFormPagePropsType<T>["propsProgressSwap"] & {
            maxW: number;
          })}
        />
      )}
      <FormProvider {...formCtx}>
        <form
          data-testid={formTestID + "__form"}
          className="form__shape"
          onSubmit={handleSave}
        >
          {children}

          <WrapFormFooter
            {...{
              propsBtnsSwapper,
              isLoading,
              submitBtnTestID: formTestID,
            }}
          />

          {typeof AdditionalFooterNode === "function" && AdditionalFooterNode()}
        </form>
      </FormProvider>
    </WrapPage>
  );
};

export default WrapFormPage;
