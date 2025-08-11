/** @jsxImportSource @emotion/react */
"use client";

import { type FC } from "react";
import { useFocus } from "@/core/hooks/etc/useFocus";
import { __cg } from "@/core/lib/log";
import { FormProvider, useForm } from "react-hook-form";
import { RegisterFormT, registerSchema } from "./schemas/register";
import { zodResolver } from "@hookform/resolvers/zod";
import BodyForm from "./components/BodyForm";
import FooterForm from "./components/FooterForm";
import { useSwap } from "@/core/hooks/etc/useSwap/useSwap";

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

  return (
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
  );
};

export default Register;
