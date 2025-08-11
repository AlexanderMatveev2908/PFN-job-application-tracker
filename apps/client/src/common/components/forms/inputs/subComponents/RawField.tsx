/** @jsxImportSource @emotion/react */
"use client";

import { FieldInputT, FormFieldTxtT, PortalConfT } from "@/common/types/ui";
import { ChangeEvent, ReactNode, RefObject, useCallback } from "react";
import {
  Control,
  Controller,
  ControllerRenderProps,
  FieldValues,
  Path,
} from "react-hook-form";
import ErrField from "../../etc/ErrField";
import { useSyncPortal } from "@/core/hooks/ui/useSyncPortal";
import Portal from "@/common/components/elements/Portal";
import { css } from "@emotion/react";

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
  portalConf?: PortalConfT;
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
  portalConf,
}: PropsType<T>) => {
  const { coords, parentRef } = useSyncPortal(portalConf?.optDep);

  const genDefProps = useCallback(
    (field: ControllerRenderProps<T, Path<T>>) => ({
      placeholder: el.place,
      disabled: !!isDisabled,
      value: field.value ?? "",
      ref: (node: HTMLInputElement | HTMLTextAreaElement | null) => {
        field.ref(node);
        parentRef.current = node;

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
    [el, cbChange, isDisabled, optRef, parentRef]
  );

  return (
    <label className="w-full grid grid-cols-1 gap-4">
      {showLabel && <span className="txt__lg">{el.label}</span>}

      <div className="w-full relative">
        <Controller
          name={el.name}
          control={control}
          render={({ field, fieldState }) => {
            const msg = fieldState?.error?.message ?? manualMsg;
            return (
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

                {typeof portalConf === "object" && portalConf !== null ? (
                  <Portal>
                    <ErrField
                      {...{
                        msg,
                        $ctmCSS: css`
                          top: ${coords.top}px;
                          right: ${coords.right}px;
                        `,
                      }}
                    />
                  </Portal>
                ) : (
                  <ErrField
                    {...{
                      msg,
                    }}
                  />
                )}
              </>
            );
          }}
        />
      </div>
    </label>
  );
};

export default RawField;
