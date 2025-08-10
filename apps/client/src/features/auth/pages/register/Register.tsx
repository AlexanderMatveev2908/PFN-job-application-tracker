/** @jsxImportSource @emotion/react */
"use client";

import { useState, type FC } from "react";
import { useFocus } from "@/core/hooks/etc/useFocus";
import { __cg } from "@/core/lib/log";
import { FormProvider, useForm } from "react-hook-form";
import { RegisterFormT, registerSchema } from "./schemas/register";
import { zodResolver } from "@hookform/resolvers/zod";
import BodyForm from "./components/BodyForm";
import FooterForm from "./components/FooterForm";

const Register: FC = ({}) => {
  const [currSwap, setCurrSwap] = useState(0);

  const formCtx = useForm<RegisterFormT>({
    mode: "onChange",
    resolver: zodResolver(registerSchema),
    defaultValues: {
      first_name: "",
      last_name: "",
      email: "",
      password: "",
      confirm_password: "",
      terms: true,
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
      <form className="w-full grid grid-cols-1 gap-10" onSubmit={handleSave}>
        <BodyForm
          {...{
            currSwap,
          }}
        />

        <FooterForm
          {...{
            currSwap,
            setCurrSwap,
          }}
        />
      </form>
    </FormProvider>
  );
};

export default Register;
