/** @jsxImportSource @emotion/react */
"use client";

import { type FC } from "react";
import { __cg } from "@/core/lib/log";
import { FormProvider, Path, useForm } from "react-hook-form";
import { RegisterFormT, registerSchema } from "./schemas/register";
import { zodResolver } from "@hookform/resolvers/zod";
import BodyForm from "./components/BodyForm";
import FooterForm from "./components/FooterForm";
import { useSwap } from "@/core/hooks/etc/useSwap/useSwap";
import { useFocusSwap } from "@/core/hooks/ui/useFocusSwap";
import { useFocus } from "@/core/hooks/ui/useFocus";
import ProgressSwap from "@/common/components/elements/ProgressSwap";

export type SwapModeT = "swapped" | "swapping" | "none";

const Register: FC = ({}) => {
  const { startSwap, swapState } = useSwap();

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

      return errs;
    }
  );

  useFocus("first_name", { setFocus });

  const kwargs: Path<RegisterFormT>[] = ["first_name", "password"];

  useFocusSwap({
    kwargs,
    setFocus,
    swapState,
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
          </form>
        </FormProvider>
      </div>
    </div>
  );
};

export default Register;
