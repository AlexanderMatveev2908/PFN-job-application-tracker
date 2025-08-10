/** @jsxImportSource @emotion/react */
"use client";

import { FormFieldTxtT } from "@/common/types/ui";
import { ChangeEvent, useCallback } from "react";
import {
  Control,
  Controller,
  ControllerRenderProps,
  FieldValues,
  Path,
} from "react-hook-form";

type PropsType<T extends FieldValues> = {
  el: FormFieldTxtT<T>;
  control: Control<T>;
  cb?: (v: string) => void;
  isDisabled?: boolean;
};

const FormFieldTxt = <T extends FieldValues>({
  el,
  control,
  cb,
  isDisabled,
}: PropsType<T>) => {
  const genDefProps = useCallback(
    (field: ControllerRenderProps<T, Path<T>>) => ({
      required: !!el.required,
      placeholder: el.place,
      disabled: isDisabled,
      value: field.value ?? "",
      className: "input__base bd__sm txt__md",

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
      {el.label && <span className="txt__lg">{el.label}</span>}

      <Controller
        name={el.name}
        control={control}
        render={({ field }) =>
          el.type === "textarea" ? (
            <textarea {...field} {...genDefProps(field)} />
          ) : (
            <input {...field} type={el.type} {...genDefProps(field)} />
          )
        }
      />
    </label>
  );
};

export default FormFieldTxt;
