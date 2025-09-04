/** @jsxImportSource @emotion/react */
"use client";

import BtnShim from "@/common/components/buttons/BtnShim/BtnShim";
import Title from "@/common/components/txt/Title";
import { ChildrenT } from "@/common/types/ui";
import { parseLabelToTestID } from "@/core/lib/etc";
import { FieldValues, FormProvider, UseFormReturn } from "react-hook-form";
import WrapSwap, { PropsTypeWrapSwap } from "../../subComponents/WrapSwap";

type PropsType<T extends FieldValues> = {
  title: string;
  formCtx: UseFormReturn<T>;
  handleSave: () => void;
  isLoading: boolean;
} & ChildrenT &
  Omit<PropsTypeWrapSwap, "children">;

const WrapSwapMultiForm = <T extends FieldValues>({
  title,
  children,
  contentRef,
  isCurr,
  formCtx,
  handleSave,
  isLoading,
}: PropsType<T>) => {
  const testID = parseLabelToTestID(title);

  return (
    <WrapSwap
      {...{
        contentRef,
        isCurr,
      }}
    >
      <FormProvider {...formCtx}>
        <form
          onSubmit={handleSave}
          data-testid={testID + "__form"}
          className="cont__grid__lg py-5"
        >
          <Title
            {...{
              title,
              $twdCls: "2xl",
            }}
          />

          {children}

          <div className="mt-[50px] w-[250px] justify-self-center">
            <BtnShim
              {...{
                type: "submit",
                label: "Submit",
                testID: testID + "__form__submit",
                isLoading,
              }}
            />
          </div>
        </form>
      </FormProvider>
    </WrapSwap>
  );
};

export default WrapSwapMultiForm;
