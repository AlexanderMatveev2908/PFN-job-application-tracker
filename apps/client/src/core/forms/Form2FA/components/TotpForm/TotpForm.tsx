/* eslint-disable @typescript-eslint/no-explicit-any */
/** @jsxImportSource @emotion/react */
"use client";

import ErrField from "@/common/components/forms/etc/ErrField";
import { PropsTypeWrapSwap } from "@/common/components/swap/components/WrapSwap";
import WrapSwapMultiForm from "@/common/components/swap/WrapMultiFormSwapper/subComponents/WrapSwapMultiForm";
import Portal from "@/common/components/wrappers/portals/Portal";
import { useFocus } from "@/core/hooks/etc/focus/useFocus";
import { useFocusMultiForm } from "@/core/hooks/etc/focus/useFocusMultiForm";
import { useSyncPortal } from "@/core/hooks/etc/tooltips/useSyncPortal";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import { SwapStateT } from "@/core/hooks/etc/useSwap/etc/initState";
import { isStr } from "@/core/lib/dataStructure";
import { ToptFormT } from "@/core/paperwork";
import { css } from "@emotion/react";
import { useEffect, useState, type FC } from "react";
import { Controller, UseFormReturn } from "react-hook-form";

type PropsType = {
  formCtx: UseFormReturn<ToptFormT>;
  handleSave: () => void;
  swapState: SwapStateT;
} & Omit<PropsTypeWrapSwap, "children">;

const TotpForm: FC<PropsType> = ({
  contentRef,
  isCurr,
  formCtx,
  handleSave,
  swapState,
}) => {
  const [focused, setFocused] = useState<number | null>(0);

  const {
    watch,
    control,
    formState: { errors },
    setFocus,
  } = formCtx;

  const code = watch();
  const realLen = code["totp_code"].filter((char) => isStr(char)).length;

  useEffect(() => {
    console.log(code);
    console.log(errors);
  }, [code, errors]);

  const { ids } = useGenIDs({ lengths: [2, 3, 3] });

  const { coords, parentRef } = useSyncPortal([swapState]);

  useFocus("totp_code.0", {
    setFocus,
  });
  useFocusMultiForm({
    keyField: `totp_code.${realLen}`,
    setFocus,
    swapState,
    targetSwap: 0,
  });

  return (
    <WrapSwapMultiForm
      {...{
        contentRef,
        isCurr,
        formCtx,
        handleSave,
        isLoading: false,
        title: "Totp Code",
      }}
    >
      <div
        ref={parentRef as any}
        className="w-fit grid grid-cols-1 items-center gap-6 sm:flex sm:justify-center justify-items-center relative mx-auto"
      >
        {Array.from({ length: 2 }).map((_, idx) => (
          <div
            key={ids[0][idx]}
            className="flex items-center justify-center gap-6"
          >
            {ids[idx + 1].map((id, innerIdx) => (
              <Controller
                key={id}
                name={`totp_code.${innerIdx + idx * 3}`}
                control={control}
                render={({ field }) => (
                  <input
                    {...field}
                    type="text"
                    value={field.value ?? ""}
                    onChange={({ target: { value } }) => {
                      field.onChange(value);
                    }}
                    onFocus={() => {}}
                    ref={(node: HTMLInputElement) => {
                      field.ref(node);
                    }}
                    className="w-[50px] h-[50px] input__base px-[15px] txt__lg"
                  />
                )}
              />
            ))}

            {isCurr && swapState.swapMode !== "swapping" && (
              <Portal>
                <ErrField
                  {...{
                    msg: errors?.totp_code?.root?.message,
                    $ctmCSS: css`
                      top: ${coords.top}px;
                      right: ${coords.right}px;
                    `,
                  }}
                />
              </Portal>
            )}
          </div>
        ))}
      </div>
    </WrapSwapMultiForm>
  );
};

export default TotpForm;
