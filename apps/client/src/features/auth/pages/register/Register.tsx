/** @jsxImportSource @emotion/react */
"use client";

import { useEffect, useRef, useState, type FC } from "react";
import { useFocus } from "@/core/hooks/etc/useFocus";
import { __cg } from "@/core/lib/log";
import { FormProvider, useForm } from "react-hook-form";
import { RegisterFormT, registerSchema } from "./schemas/register";
import { zodResolver } from "@hookform/resolvers/zod";
import BodyForm from "./components/BodyForm";
import FooterForm from "./components/FooterForm";
import { clearTmr } from "@/core/lib/etc";

export type SwapModeT = "swapped" | "swapping" | "none";

const Register: FC = ({}) => {
  const [currSwap, setCurrSwap] = useState(0);
  const [swapMode, setSwapMode] = useState<SwapModeT>("none");
  const timerID = useRef<NodeJS.Timeout>(null);

  useEffect(() => {
    timerID.current = setTimeout(() => {
      setSwapMode("swapped");

      clearTmr(timerID);
    }, 400);

    return () => {
      clearTmr(timerID);
    };
  }, [currSwap, swapMode]);

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
            currSwap,
            swapMode,
          }}
        />

        <FooterForm
          {...{
            currSwap,
            setCurrSwap,
            setSwapMode,
          }}
        />
      </form>
    </FormProvider>
  );
};

export default Register;
