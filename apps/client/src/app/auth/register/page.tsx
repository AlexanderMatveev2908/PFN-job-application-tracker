"use client";

import WrapAuthForm from "@/features/auth/components/WrapAuthForm";
import {
  RegisterFormT,
  registerSchema,
} from "@/features/auth/schemas/register";
import { useEffect, type FC } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import { registerField } from "@/features/auth/uiFactory/register";
import { useFocus } from "@/core/hooks/etc/useFocus";
import { __cg } from "@/core/lib/log";

const Page: FC = () => {
  const formCtx = useForm<RegisterFormT>({
    mode: "onChange",
    resolver: zodResolver(registerSchema),
  });
  const {
    control,
    setFocus,
    watch,
    formState: { errors },
  } = formCtx;

  useFocus("first_name", { setFocus });

  const vls = watch();
  useEffect(() => {
    __cg(vls);
  }, [vls]);

  return (
    <WrapAuthForm>
      <FormFieldTxt
        {...{
          el: registerField,
          control,
          errors,
        }}
      />
    </WrapAuthForm>
  );
};

export default Page;
