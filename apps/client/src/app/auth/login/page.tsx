"use client";

import { useWrapAPI } from "@/core/hooks/api/useWrapAPI";
import { useFocus } from "@/core/hooks/ui/useFocus";
import { __cg } from "@/core/lib/log";
import AuthFormFooter from "@/features/auth/components/AuthFormFooter";
import AuthFormWrap from "@/features/auth/components/AuthFormWrap";
import AuthPageWrap from "@/features/auth/components/AuthPageWrap";
import BodyFormLogin from "@/features/auth/pages/login/components/BodyFormLogin";
import {
  LoginFormT,
  loginSchema,
  resetValsLogin,
} from "@/features/auth/pages/login/paperwork";
import { authSliceAPI, LoginUserReturnT } from "@/features/auth/slices/api";
import { useEndPendingActionUser } from "@/features/user/hooks/useEndPendingActionUser";
import { useUser } from "@/features/user/hooks/useUser";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { FC } from "react";
import { useForm } from "react-hook-form";

const Page: FC = () => {
  useEndPendingActionUser();

  const { wrapAPI } = useWrapAPI();
  const nav = useRouter();
  const [mutate, { isLoading }] = authSliceAPI.useLoginUserMutation();
  const { loginUser } = useUser();

  const formCtx = useForm<LoginFormT>({
    mode: "onChange",
    resolver: zodResolver(loginSchema),
    defaultValues: resetValsLogin,
  });
  const { handleSubmit, setFocus, reset } = formCtx;

  const handleSave = handleSubmit(
    async (data) => {
      const res = await wrapAPI<LoginUserReturnT>({
        cbAPI: () => mutate(data),
      });

      if (res.isErr) return;

      if (res.access_token) loginUser(res.access_token);

      reset(resetValsLogin);

      nav.replace("/");
    },
    (errs) => {
      __cg("errs", errs);
      return errs;
    }
  );

  useFocus("email", { setFocus });

  return (
    <AuthPageWrap>
      <AuthFormWrap
        {...{
          formCtx,
          handleSave,
          formTestID: "login",
        }}
      >
        <BodyFormLogin />

        <AuthFormFooter
          {...{
            isLoading,
            submitBtnTestID: "login",
          }}
        />
      </AuthFormWrap>
    </AuthPageWrap>
  );
};

export default Page;
