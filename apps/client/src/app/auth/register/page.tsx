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
import { registerSwap_0 } from "@/features/auth/uiFactory/register";
import { useFocus } from "@/core/hooks/etc/useFocus";
import { __cg } from "@/core/lib/log";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";

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

  const { ids } = useGenIDs({
    lengths: [registerSwap_0.length],
  });

  return (
    <WrapAuthForm>
      <div className="w-full grid grid-cols-1 gap-6">
        {registerSwap_0.map((el, i) => (
          <FormFieldTxt
            key={ids[0][i]}
            {...{
              el,
              control,
              errors,
            }}
          />
        ))}
      </div>
    </WrapAuthForm>
  );
};

export default Page;
