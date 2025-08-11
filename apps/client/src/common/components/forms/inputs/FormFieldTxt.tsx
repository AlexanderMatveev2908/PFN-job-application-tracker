/** @jsxImportSource @emotion/react */
"use client";

import { RawFieldPropsT } from "@/common/types/ui";
import { FieldValues } from "react-hook-form";
import RawField from "./subComponents/RawField";

const FormFieldTxt = <T extends FieldValues>({
  el,
  control,
  cbChange,
  isDisabled,
  manualMsg,
  optRef,
  cbFocus,
  cbBlur,
  showLabel = true,
  portalConf,
}: RawFieldPropsT<T>) => {
  return (
    <RawField
      {...{
        el,
        control,
        cbChange,
        cbFocus,
        cbBlur,
        isDisabled,
        manualMsg,
        showLabel,
        optRef,
        portalConf,
      }}
    />
  );
};

export default FormFieldTxt;
