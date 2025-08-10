/** @jsxImportSource @emotion/react */
"use client";

import { FormFieldTxtT } from "@/common/types/ui";
import { ChangeEvent, CSSProperties, useCallback } from "react";
import {
  Control,
  Controller,
  ControllerRenderProps,
  FieldErrors,
  FieldValues,
  Path,
} from "react-hook-form";
import ErrField from "../etc/ErrField";
import { FaLock, FaLockOpen } from "react-icons/fa6";

type PropsType<T extends FieldValues> = {
  el: FormFieldTxtT<T>;
  control: Control<T>;
  cb?: (v: string) => void;
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
  cb,
  isDisabled,
  errors,
  manualMsg,
  showLabel = true,
  isShw,
  handleSvgClick,
}: PropsType<T>) => {
  const msg = manualMsg ?? (errors?.[el.name]?.message as string);

  const genDefProps = useCallback(
    (field: ControllerRenderProps<T, Path<T>>) => ({
      placeholder: el.place,
      disabled: isDisabled,
      value: field.value ?? "",
      className: "input__base txt__md",

      onChange: (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const {
          target: { value: v },
        } = e;

        field.onChange(v);

        cb?.(v);
      },
    }),
    [el, cb, isDisabled]
  );

  const Svg = isShw ? FaLockOpen : FaLock;

  return (
    <label className="w-full grid grid-cols-1 gap-4">
      {showLabel && <span className="txt__lg">{el.label}</span>}

      <div className="w-full relative">
        <Controller
          name={el.name}
          control={control}
          render={({ field }) => (
            <input
              {...field}
              type={isShw ? "text" : "password"}
              {...genDefProps(field)}
            />
          )}
        />

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

        <ErrField
          {...{
            msg,
          }}
        />
      </div>
    </label>
  );
};

export default FormFieldPwd;
