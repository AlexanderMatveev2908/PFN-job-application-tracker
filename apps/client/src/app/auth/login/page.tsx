"use client";

import { useWrapAPI } from "@/core/hooks/api/useWrapAPI";
import { useFocus } from "@/core/hooks/etc/focus/useFocus";
import { logFormErrs } from "@/core/lib/etc";
import WrapFormPage from "@/common/components/forms/shapes/WrapFormPage";
import BodyFormLogin from "@/features/auth/pages/login/components/BodyFormLogin";
import {
  LoginFormT,
  loginSchema,
  resetValsLogin,
} from "@/features/auth/pages/login/paperwork";
import { authSliceAPI, LoginUserReturnT } from "@/features/auth/slices/api";
import { useUser } from "@/features/user/hooks/useUser";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { FC } from "react";
import { useForm } from "react-hook-form";

const Page: FC = () => {
  const { wrapAPI } = useWrapAPI();
  const nav = useRouter();
  const [mutate, { isLoading }] = authSliceAPI.useLoginAuthMutation();
  const { loginUser } = useUser();

  const formCtx = useForm<LoginFormT>({
    mode: "onChange",
    resolver: zodResolver(loginSchema),
    defaultValues: resetValsLogin,
  });
  const { handleSubmit, setFocus, reset } = formCtx;

  const handleSave = handleSubmit(async (data) => {
    const res = await wrapAPI<LoginUserReturnT>({
      cbAPI: () => mutate(data),
    });

    if (res?.isErr) return;

    if (res?.access_token) {
      loginUser(res.access_token);

      reset(resetValsLogin);

      nav.replace("/");
    }
  }, logFormErrs);

  useFocus("email", { setFocus });

  return (
    <WrapFormPage
      {...{
        formCtx,
        handleSave,
        formTestID: "login",
        isLoading,
      }}
    >
      <BodyFormLogin />
    </WrapFormPage>
  );
};

export default Page;
