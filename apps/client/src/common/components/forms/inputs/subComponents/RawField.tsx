/** @jsxImportSource @emotion/react */
"use client";

import { FieldInputT, FormFieldTxtT } from "@/common/types/ui";
import { ChangeEvent, ReactNode, RefObject, useCallback } from "react";
import {
  Control,
  Controller,
  ControllerRenderProps,
  FieldValues,
  Path,
} from "react-hook-form";
import ErrField from "../../etc/ErrField";

type PropsType<T extends FieldValues> = {
  el: FormFieldTxtT<T>;
  control: Control<T>;
  cbChange?: (v: string) => void;
  isDisabled?: boolean;
  manualMsg?: string;
  showLabel?: boolean;
  dynamicInputT?: FieldInputT;
  children?: ReactNode;
  optRef?: RefObject<HTMLElement | null>;
};

const RawField = <T extends FieldValues>({
  el,
  cbChange,
  isDisabled,
  manualMsg,
  showLabel,
  children,
  control,
  dynamicInputT,
  optRef,
}: PropsType<T>) => {
  const genDefProps = useCallback(
    (field: ControllerRenderProps<T, Path<T>>) => ({
      placeholder: el.place,
      disabled: !!isDisabled,
      value: field.value ?? "",
      ref: (node: HTMLInputElement | HTMLTextAreaElement | null) => {
        field.ref(node);

        if (optRef) optRef.current = node;
      },
      className: `input__base txt__md ${
        el.type === "textarea" && "scroll__app"
      }`,

      onChange: (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const {
          target: { value: v },
        } = e;

        field.onChange(v);

        cbChange?.(v);
      },
    }),
    [el, cbChange, isDisabled, optRef]
  );

  return (
    <label className="w-full grid grid-cols-1 gap-4">
      {showLabel && <span className="txt__lg">{el.label}</span>}

      <div className="w-full relative">
        <Controller
          name={el.name}
          control={control}
          render={({ field, fieldState }) => (
            <>
              {el.type === "textarea" ? (
                <textarea {...field} {...genDefProps(field)} rows={4} />
              ) : (
                <input
                  {...field}
                  type={dynamicInputT ?? el.type}
                  {...genDefProps(field)}
                />
              )}

              {children}

              <ErrField
                {...{
                  msg: fieldState?.error?.message ?? manualMsg,
                }}
              />
            </>
          )}
        />
      </div>
    </label>
  );
};

export default RawField;
