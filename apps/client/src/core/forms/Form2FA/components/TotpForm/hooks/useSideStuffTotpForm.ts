import { REG_INT } from "@/core/constants/regex";
import { ToptFormT } from "@/core/paperwork";
import { useEffect, useState } from "react";
import {
  UseFormSetFocus,
  UseFormSetValue,
  UseFormTrigger,
} from "react-hook-form";

type Params = {
  setValue: UseFormSetValue<ToptFormT>;
  setFocus: UseFormSetFocus<ToptFormT>;
  trigger: UseFormTrigger<ToptFormT>;
  totp_code: string[];
};

export const useSideStuffTotpForm = ({
  setValue,
  setFocus,
  trigger,
  totp_code,
}: Params) => {
  const [ctrlPressed, setCtrlPressed] = useState<boolean>();
  const [currFocus, setCurrFocus] = useState<number | null>(null);

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
        trigger();
        return;
      }

      if (e.key === "Backspace" && typeof currFocus === "number") {
        setValue(
          "totp_code",
          totp_code.map((v, idx) => (idx === currFocus ? "" : v)),
          { shouldValidate: true }
        );
        setFocus(`totp_code.${currFocus - 1 >= 0 ? currFocus - 1 : 0}`);
        trigger();
        return;
      }

      if (REG_INT.test(e.key) && typeof currFocus === "number") {
        setValue(
          "totp_code",
          totp_code.map((v, idx) => (idx === currFocus ? e.key : v)),
          { shouldValidate: true }
        );
        setFocus(`totp_code.${Math.min(currFocus + 1, 5)}`);
        trigger();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [ctrlPressed, currFocus, totp_code, setValue, setFocus, trigger]);

  return {
    ctrlPressed,
    setCtrlPressed,
    setCurrFocus,
  };
};
