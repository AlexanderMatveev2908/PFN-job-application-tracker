/** @jsxImportSource @emotion/react */
"use client";

import { FormFieldTxtT } from "@/common/types/ui";
import { ChangeEvent, useCallback } from "react";
import {
  Control,
  Controller,
  ControllerRenderProps,
  FieldErrors,
  FieldValues,
  Path,
} from "react-hook-form";
import ErrField from "../etc/ErrField";

type PropsType<T extends FieldValues> = {
  el: FormFieldTxtT<T>;
  control: Control<T>;
  cb?: (v: string) => void;
  isDisabled?: boolean;
  errors?: FieldErrors<T>;
  manualMsg?: string;
  showLabel?: boolean;
};

const FormFieldTxt = <T extends FieldValues>({
  el,
  control,
  cb,
  isDisabled,
  errors,
  manualMsg,
  showLabel = true,
}: PropsType<T>) => {
  const msg = manualMsg ?? (errors?.[el.name]?.message as string);

  const genDefProps = useCallback(
    (field: ControllerRenderProps<T, Path<T>>) => ({
      placeholder: el.place,
      disabled: isDisabled,
      value: field.value ?? "",
      className: `input__base txt__md ${
        el.type === "textarea" && "scroll__app"
      }`,

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

  return (
    <label className="w-full grid grid-cols-1 gap-4">
      {showLabel && <span className="txt__lg">{el.label}</span>}

      <div className="w-full relative">
        <Controller
          name={el.name}
          control={control}
          render={({ field }) =>
            el.type === "textarea" ? (
              <textarea {...field} {...genDefProps(field)} rows={4} />
            ) : (
              <input {...field} type={el.type} {...genDefProps(field)} />
            )
          }
        />

        <ErrField
          {...{
            msg,
          }}
        />
      </div>
    </label>
  );
};

export default FormFieldTxt;
