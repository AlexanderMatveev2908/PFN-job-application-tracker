/** @jsxImportSource @emotion/react */
"use client";

import { FormFieldTxtT } from "@/common/types/ui";
import { Control, FieldValues } from "react-hook-form";
import RawField from "./subComponents/RawField";
import { RefObject } from "react";

type PropsType<T extends FieldValues> = {
  el: FormFieldTxtT<T>;
  control: Control<T>;
  cbChange?: (v: string) => void;
  isDisabled?: boolean;
  manualMsg?: string;
  showLabel?: boolean;
  optRef?: RefObject<HTMLElement | null>;
};

const FormFieldTxt = <T extends FieldValues>({
  el,
  control,
  cbChange,
  isDisabled,
  manualMsg,
  optRef,
  showLabel = true,
}: PropsType<T>) => {
  return (
    <RawField
      {...{
        el,
        control,
        cbChange,
        isDisabled,
        manualMsg,
        showLabel,
        optRef,
      }}
    />
  );
};

export default FormFieldTxt;
