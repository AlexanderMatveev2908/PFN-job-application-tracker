/** @jsxImportSource @emotion/react */
"use client";

import { RawFieldPropsT } from "@/common/types/ui";
import { CSSProperties } from "react";
import { FieldValues } from "react-hook-form";
import { FaLock, FaLockOpen } from "react-icons/fa6";
import RawField from "./subComponents/RawField";

type PropsType<T extends FieldValues> = {
  isShw: boolean;
  handleSvgClick: () => void;
} & RawFieldPropsT<T>;

const FormFieldPwd = <T extends FieldValues>({
  el,
  control,
  cbChange,
  isDisabled,
  manualMsg,
  showLabel = true,
  isShw,
  handleSvgClick,
  optRef,
  portalConf,
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
        optRef,
        dynamicInputT: isShw ? "text" : "password",
        portalConf,
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
