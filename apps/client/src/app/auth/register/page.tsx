/** @jsxImportSource @emotion/react */
"use client";

import { type FC } from "react";
import { __cg } from "@/core/lib/log";
import { FormProvider, Path, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useSwap } from "@/core/hooks/etc/useSwap/useSwap";
import ProgressSwap from "@/common/components/elements/ProgressSwap";
import BodyForm from "@/features/auth/pages/register/components/BodyForm";
import FooterForm from "@/features/auth/pages/register/components/FooterForm";
import {
  RegisterFormT,
  registerSchema,
} from "@/features/auth/pages/register/schemas/register";
import SpannerLinks from "@/features/auth/components/SpannerLinks/SpannerLinks";
import { swapOnErr } from "@/core/lib/forms";
import { authSliceAPI } from "@/features/auth/slices/sliceAPI";
import { useWrapMutation } from "@/core/hooks/api/useWrapMutation";
import { useRouter } from "next/navigation";
import { useNotice } from "@/features/notice/hooks/useNotice";
import { genLorem } from "@/core/lib/etc";
import { saveStorage } from "@/core/lib/storage";
import { useUs } from "@/features/user/hooks/useUs";

export type SwapModeT = "swapped" | "swapping" | "none";

const Register: FC = ({}) => {
  const formCtx = useForm<RegisterFormT>({
    mode: "onChange",
    resolver: zodResolver(registerSchema),
    defaultValues: {
      // first_name: "",
      // last_name: "",
      // email: "",
      // password: "",
      // confirm_password: "",
      // terms: false,
      first_name: "Alex",
      last_name: "Matveev",
      email: "matveevalexander470@gmail.com",
      password: "0$EM09btNPiC}!3d+t2{",
      confirm_password: "0$EM09btNPiC}!3d+t2{",
      terms: true,
    },
  });
  const { setFocus, handleSubmit } = formCtx;

  const [mutate, { isLoading }] = authSliceAPI.useRegisterUserMutation();
  const { wrapMutation } = useWrapMutation();
  const { setNotice } = useNotice();
  const { loginUser } = useUs();
  const nav = useRouter();

  const kwargs: Path<RegisterFormT>[] = ["first_name", "password"];

  const { startSwap, swapState } = useSwap({
    setFocus,
    kwargs,
  });

  const handleSave = handleSubmit(
    async (data) => {
      const res = await wrapMutation({
        cbAPI: () => mutate(data),
      });

      if (!res) return;

      loginUser(res.access_token);

      setNotice({
        msg: "We've sent you an email to confirm the account. If you don't see it, check your spam folder, it might be partying there 🎉",
        type: "OK",
        keyCb: "LOGIN",
      });

      nav.replace("/notice");
    },
    (errs) => {
      __cg("errors", errs);

      const res = swapOnErr({
        errs,
        kwargs: [
          ["first_name", "last_name", "email"],
          ["password", "confirm_password", "terms"],
        ],
      });

      if (res?.field) {
        startSwap({ swap: res!.i, lockFocus: true });
        setTimeout(() => {
          setFocus(res.field);
        }, 400);
      }

      return errs;
    }
  );

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
          <form
            data-testid={"register_form"}
            className="w-full grid grid-cols-1"
            onSubmit={handleSave}
          >
            <BodyForm
              {...{
                swapState,
              }}
            />

            <FooterForm
              {...{
                swapState,
                startSwap,
                isLoading,
              }}
            />

            <SpannerLinks />
          </form>
        </FormProvider>
      </div>
    </div>
  );
};

export default Register;
