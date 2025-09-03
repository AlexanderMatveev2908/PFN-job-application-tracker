/** @jsxImportSource @emotion/react */
"use client";

import ProgressSwap from "@/common/components/swap/subComponents/ProgressSwap";
import { ChildrenT } from "@/common/types/ui";
import { isObjOk } from "@/core/lib/dataStructure";
import { FieldValues, FormProvider, UseFormReturn } from "react-hook-form";
import WrapFormFooter from "./subComponents/WrapFormFooter";
import { PropsTypeBtnsSwapper } from "../../swap/subComponents/BtnsSwapper";
import WrapPage from "../../HOC/pageWrappers/WrapPage";
import { ReactNode } from "react";

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
          className="cont__grid__md"
          onSubmit={handleSave}
        >
          <div className="form__shape">
            {children}

            <WrapFormFooter
              {...{
                propsBtnsSwapper,
                isLoading,
                submitBtnTestID: formTestID,
              }}
            />

            {typeof AdditionalFooterNode === "function" &&
              AdditionalFooterNode()}
          </div>
        </form>
      </FormProvider>
    </WrapPage>
  );
};

export default WrapFormPage;
