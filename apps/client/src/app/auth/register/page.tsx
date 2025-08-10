"use client";

import WrapAuthForm from "@/features/auth/components/WrapAuthForm";
import {
  RegisterFormT,
  registerSchema,
} from "@/features/auth/schemas/register";
import type { FC } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import { registerField } from "@/features/auth/uiFactory/register";

const Page: FC = () => {
  const formCtx = useForm<RegisterFormT>({
    mode: "onChange",
    resolver: zodResolver(registerSchema),
  });

  return (
    <WrapAuthForm>
      <FormFieldTxt
        {...{
          el: registerField,
        }}
      />
    </WrapAuthForm>
  );
};

export default Page;
