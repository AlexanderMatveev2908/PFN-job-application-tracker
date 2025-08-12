/** @jsxImportSource @emotion/react */
"use client";

import { useRef, type FC } from "react";
import { __cg } from "@/core/lib/log";
import { FormProvider, Path, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useSwap } from "@/core/hooks/etc/useSwap/useSwap";
import { useFocusSwap } from "@/core/hooks/ui/useFocusSwap";
import { useFocus } from "@/core/hooks/ui/useFocus";
import ProgressSwap from "@/common/components/elements/ProgressSwap";
import BodyForm from "@/features/auth/pages/register/components/BodyForm";
import FooterForm from "@/features/auth/pages/register/components/FooterForm";
import {
  RegisterFormT,
  registerSchema,
} from "@/features/auth/pages/register/schemas/register";
import SpannerLinks from "@/features/auth/components/SpannerLinks/SpannerLinks";
import { swapOnErr } from "@/core/lib/forms";

export type SwapModeT = "swapped" | "swapping" | "none";

const Register: FC = ({}) => {
  const { startSwap, swapState } = useSwap();

  const lockFocusRef = useRef<boolean>(false);

  const lockFocus = (ms: number = 600) => {
    lockFocusRef.current = true;
    const t = setTimeout(() => {
      lockFocusRef.current = false;
      clearTimeout(t);
    }, ms);
  };

  const formCtx = useForm<RegisterFormT>({
    mode: "onChange",
    resolver: zodResolver(registerSchema),
    defaultValues: {
      first_name: "",
      last_name: "",
      email: "",
      password: "",
      confirm_password: "",
      terms: false,
    },
  });

  const { setFocus, handleSubmit } = formCtx;

  const handleSave = handleSubmit(
    (data) => {
      __cg(data);
    },
    (errs) => {
      __cg("errors", errs);

      const res = swapOnErr({
        errs,
        kwargs: [
          ["first_name", "last_name", "email"],
          ["password", "confirm_password", "terms"],
        ],
      });

      if (res?.field) {
        startSwap({ swap: res!.i, manualFocus: true });
        lockFocus();
        setTimeout(() => {
          setFocus(res.field);
        }, 400);
      }

      return errs;
    }
  );

  useFocus("first_name", { setFocus });

  const kwargs: Path<RegisterFormT>[] = ["first_name", "password"];

  useFocusSwap({
    kwargs,
    setFocus,
    swapState,
    lockFocusRef,
  });

  return (
    <div className="w-full grid grid-cols-1 gap-10 mt-[20px]">
      <ProgressSwap
        {...{
          currSwap: swapState.currSwap,
          maxW: 800,
          totSwaps: 2,
        }}
      />
      <div className="auth__form">
        <FormProvider {...formCtx}>
          <form className="w-full grid grid-cols-1" onSubmit={handleSave}>
            <BodyForm
              {...{
                swapState,
              }}
            />

            <FooterForm
              {...{
                swapState,
                startSwap,
              }}
            />

            <SpannerLinks />
          </form>
        </FormProvider>
      </div>
    </div>
  );
};

export default Register;
