/* eslint-disable @typescript-eslint/no-explicit-any */
/** @jsxImportSource @emotion/react */
"use client";

import ErrField from "@/common/components/forms/etc/ErrField";
import { PropsTypeWrapSwap } from "@/common/components/swap/components/WrapSwap";
import WrapSwapMultiForm from "@/common/components/swap/WrapMultiFormSwapper/subComponents/WrapSwapMultiForm";
import Portal from "@/common/components/wrappers/portals/Portal";
import { REG_INT } from "@/core/constants/regex";
import { useFocus } from "@/core/hooks/etc/focus/useFocus";
import { useSyncPortal } from "@/core/hooks/etc/tooltips/useSyncPortal";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import { SwapStateT } from "@/core/hooks/etc/useSwap/etc/initState";
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
  const [ctrlPressed, setCtrlPressed] = useState<boolean>();
  const [currFocus, setCurrFocus] = useState<number | null>(null);

  const {
    watch,
    control,
    formState: { errors },
    setFocus,
    setValue,
  } = formCtx;

  const code = watch();
  // const realLength = code["totp_code"].filter((ch) => isStr(ch)).length;

  const { ids } = useGenIDs({ lengths: [2, 3, 3] });

  const { coords, parentRef } = useSyncPortal([swapState]);

  useFocus("totp_code.0", {
    setFocus,
  });

  useEffect(() => {
    const handlePaste = (e: ClipboardEvent) => {
      e.preventDefault();

      const pasted = e.clipboardData?.getData("text") ?? "";
      const parsed = pasted.split("").slice(0, 6);

      setValue("totp_code", parsed, { shouldValidate: true });
    };

    window.addEventListener("paste", handlePaste);

    return () => {
      window.removeEventListener("paste", handlePaste);
    };
  }, [setValue]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const defVals = Array(6).fill("");

      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "a") {
        setCtrlPressed(true);
        return;
      }

      if (ctrlPressed) {
        const possibleVal = e.key.trim();

        if (e.key === "Backspace" || !possibleVal) {
          setValue("totp_code", defVals, { shouldValidate: true });
        } else {
          setValue("totp_code", [possibleVal, ...Array(5).fill("")], {
            shouldValidate: true,
          });
        }

        setCtrlPressed(false);
        setFocus("totp_code.0");
        return;
      }

      if (e.key === "Backspace" && typeof currFocus === "number") {
        setValue(
          "totp_code",
          code.totp_code.map((v, idx) => (idx === currFocus ? "" : v)),
          { shouldValidate: true }
        );
        setFocus(`totp_code.${currFocus - 1 >= 0 ? currFocus - 1 : 0}`);
        return;
      }

      if (REG_INT.test(e.key) && typeof currFocus === "number") {
        setValue(
          "totp_code",
          code.totp_code.map((v, idx) => (idx === currFocus ? e.key : v)),
          { shouldValidate: true }
        );
        setFocus(`totp_code.${Math.min(currFocus + 1, 5)}`);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [ctrlPressed, currFocus, code.totp_code, setValue, setFocus]);

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
                    // eslint-disable-next-line @typescript-eslint/no-unused-vars
                    onChange={({ target: { value: v } }) => {
                      // if (v.length > 1) return;
                      // field.onChange(v);
                      // if (isStr(v)) setFocus(`totp_code.${realLength + 1}`);
                    }}
                    onFocus={() => {
                      setCurrFocus(innerIdx + idx * 3);
                    }}
                    onBlur={() => {
                      setCtrlPressed(false);
                      setCurrFocus(null);
                    }}
                    ref={(node: HTMLInputElement) => {
                      field.ref(node);
                    }}
                    className={`w-[50px] h-[50px] input__base px-[15px] txt__lg ${
                      ctrlPressed ? "text-black bg-w__0" : ""
                    }`}
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
