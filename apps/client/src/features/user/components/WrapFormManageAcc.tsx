/** @jsxImportSource @emotion/react */
"use client";

import BtnShim from "@/common/components/buttons/BtnShim/BtnShim";
import Title from "@/common/components/elements/txt/Title";
import WrapSwap, {
  PropsTypeWrapSwap,
} from "@/common/components/swap/subComponents/WrapSwap";
import { ChildrenT } from "@/common/types/ui";
import { parseLabelToTestID } from "@/core/lib/etc";
import { FieldValues, FormProvider, UseFormReturn } from "react-hook-form";

type PropsType<T extends FieldValues> = {
  title: string;
  formCtx: UseFormReturn<T>;
  handleSave: () => void;
} & ChildrenT &
  Omit<PropsTypeWrapSwap, "children">;

const WrapFormManageAcc = <T extends FieldValues>({
  title,
  children,
  contentRef,
  isCurr,
  formCtx,
  handleSave,
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
          className="form__container pt-5 gap-8"
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
                isLoading: false,
              }}
            />
          </div>
        </form>
      </FormProvider>
    </WrapSwap>
  );
};

export default WrapFormManageAcc;
