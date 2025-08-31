"use client";

import { __cg } from "@/core/lib/log";
import AuthFormFooter from "@/features/auth/components/AuthFormFooter";
import AuthFormWrap from "@/features/auth/components/AuthFormWrap";
import AuthPageWrap from "@/features/auth/components/AuthPageWrap";
import {
  LoginFormT,
  loginSchema,
  resetValsLogin,
} from "@/features/auth/pages/login/paperwork";
import { useEndPendingActionUser } from "@/features/user/hooks/useEndPendingActionUser";
import { zodResolver } from "@hookform/resolvers/zod";
import { FC } from "react";
import { useForm } from "react-hook-form";

const Page: FC = () => {
  useEndPendingActionUser();

  const formCtx = useForm<LoginFormT>({
    mode: "onBlur",
    resolver: zodResolver(loginSchema),
    defaultValues: resetValsLogin,
  });
  const { handleSubmit } = formCtx;

  const handleSave = handleSubmit(
    async (data) => {
      __cg("data", data);
    },
    (errs) => {
      __cg("errs", errs);
      return errs;
    }
  );

  return (
    <AuthPageWrap>
      <AuthFormWrap
        {...{
          formCtx,
          handleSave,
          formTestID: "login",
        }}
      >
        <AuthFormFooter
          {...{
            isLoading: false,
            submitBtnTestID: "login",
          }}
        />
      </AuthFormWrap>
    </AuthPageWrap>
  );
};

export default Page;
