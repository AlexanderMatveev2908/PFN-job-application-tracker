/** @jsxImportSource @emotion/react */
"use client";

import { FormFieldTxtT } from "@/common/types/ui";
import { CSSProperties } from "react";
import { Control, FieldErrors, FieldValues } from "react-hook-form";
import { FaLock, FaLockOpen } from "react-icons/fa6";
import RawField from "./subComponents/RawField";

type PropsType<T extends FieldValues> = {
  el: FormFieldTxtT<T>;
  control: Control<T>;
  cbChange?: (v: string) => void;
  isDisabled?: boolean;
  errors?: FieldErrors<T>;
  manualMsg?: string;
  showLabel?: boolean;

  isShw: boolean;
  handleSvgClick: () => void;
};

const FormFieldPwd = <T extends FieldValues>({
  el,
  control,
  cbChange,
  isDisabled,
  manualMsg,
  showLabel = true,
  isShw,
  handleSvgClick,
}: PropsType<T>) => {
  const Svg = isShw ? FaLockOpen : FaLock;

  return (
    <RawField
      {...{
        el,
        control,
        cbChange,
        isDisabled,
        manualMsg,
        showLabel,
        dynamicInputT: isShw ? "text" : "password",
      }}
    >
      <button
        onClick={handleSvgClick}
        type="button"
        className="btn__app absolute top-1/2 -translate-y-1/2 right-4"
        style={
          {
            "--scale__up": 1.2,
          } as CSSProperties
        }
      >
        <Svg className="svg__xxs" />
      </button>
    </RawField>
  );
};

export default FormFieldPwd;
