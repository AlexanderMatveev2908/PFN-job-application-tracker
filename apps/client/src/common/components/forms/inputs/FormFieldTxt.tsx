/** @jsxImportSource @emotion/react */
"use client";

import { FormFieldTxtT } from "@/common/types/ui";
import { Control, FieldValues } from "react-hook-form";
import RawField from "./subComponents/RawField";

type PropsType<T extends FieldValues> = {
  el: FormFieldTxtT<T>;
  control: Control<T>;
  cbChange?: (v: string) => void;
  isDisabled?: boolean;
  manualMsg?: string;
  showLabel?: boolean;
};

const FormFieldTxt = <T extends FieldValues>({
  el,
  control,
  cbChange,
  isDisabled,
  manualMsg,
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
      }}
    />
  );
};

export default FormFieldTxt;
