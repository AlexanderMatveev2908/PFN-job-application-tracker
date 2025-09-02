/** @jsxImportSource @emotion/react */
"use client";

import ProgressSwap from "@/common/components/swap/ProgressSwap";
import { ChildrenT } from "@/common/types/ui";
import { isObjOk } from "@/core/lib/dataStructure";
import { FieldValues, FormProvider, UseFormReturn } from "react-hook-form";
import WrapFormFooter from "./subComponents/WrapFormFooter";
import { PropsTypeBtnsSwapper } from "../../swap/BtnsSwapper";

type PropsType<T extends FieldValues> = {
  propsProgressSwap?: {
    currSwap: number;
    totSwaps: number;
  };
  propsBtnsSwapper?: PropsTypeBtnsSwapper;
  formCtx: UseFormReturn<T>;
  handleSave: () => void;
  formTestID: string;
  isLoading: boolean;
} & ChildrenT;

const WrapFormPage = <T extends FieldValues>({
  propsProgressSwap,
  children,
  formCtx,
  handleSave,
  formTestID,
  isLoading,
  propsBtnsSwapper,
}: PropsType<T>) => {
  return (
    <div className="w-full grid grid-cols-1 gap-10 mt-[20px]">
      {isObjOk(propsProgressSwap) && (
        <ProgressSwap
          {...({
            maxW: 800,
            ...propsProgressSwap,
          } as PropsType<T>["propsProgressSwap"] & { maxW: number })}
        />
      )}
      <FormProvider {...formCtx}>
        <form
          data-testid={formTestID + "__form"}
          className="w-full grid grid-cols-1"
          onSubmit={handleSave}
        >
          <div className="w-full mx-auto max-w-[800px] h-fit rounded-xl border-3 border-neutral-300">
            {children}

            <WrapFormFooter
              {...{
                propsBtnsSwapper,
                isLoading,
                submitBtnTestID: formTestID,
              }}
            />
          </div>
        </form>
      </FormProvider>
    </div>
  );
};

export default WrapFormPage;
