/** @jsxImportSource @emotion/react */
"use client";

import { type FC } from "react";
import { __cg } from "@/core/lib/log";
import { Path, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useSwap } from "@/core/hooks/etc/useSwap/useSwap";
import BodyFormRegister from "@/features/auth/pages/register/components/BodyFormRegister";
import {
  RegisterFormT,
  registerSchema,
  resetValsRegister,
} from "@/features/auth/pages/register/paperwork";
import { swapOnErr } from "@/core/lib/forms";
import { authSliceAPI, RegisterUserReturnT } from "@/features/auth/slices/api";
import { useRouter } from "next/navigation";
import { useNotice } from "@/features/notice/hooks/useNotice";
import { useUser } from "@/features/user/hooks/useUser";
import { genMailNoticeMsg } from "@/core/constants/etc";
import { useWrapAPI } from "@/core/hooks/api/useWrapAPI";
import WrapFormPage from "@/common/components/forms/shapes/WrapFormPage";
import WrapFormFooter from "@/common/components/forms/shapes/WrapFormFooter";
import WrapForm from "@/common/components/forms/shapes/WrapForm";

export type SwapModeT = "swapped" | "swapping" | "none";

const Page: FC = () => {
  const formCtx = useForm<RegisterFormT>({
    mode: "onChange",
    resolver: zodResolver(registerSchema),
    defaultValues: resetValsRegister,
  });
  const { setFocus, handleSubmit, reset } = formCtx;

  const [mutate, { isLoading }] = authSliceAPI.useRegisterAuthMutation();
  const { wrapAPI } = useWrapAPI();
  const { setNotice } = useNotice();
  const { loginUser } = useUser();
  const nav = useRouter();

  const kwargs: Path<RegisterFormT>[] = ["first_name", "password"];

  const { startSwap, swapState } = useSwap({
    setFocus,
    kwargs,
  });

  const handleSave = handleSubmit(
    async (data) => {
      const res = await wrapAPI<RegisterUserReturnT>({
        cbAPI: () => mutate(data),
      });

      if (res?.isErr) return;

      reset(resetValsRegister);

      loginUser(res!.access_token);

      setNotice({
        msg: genMailNoticeMsg("to confirm the account"),
        type: "OK",
        child: "OPEN_MAIL_APP",
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
    <WrapFormPage
      {...{
        propsProgressSwap: {
          currSwap: swapState.currSwap,
          totSwaps: 2,
        },
      }}
    >
      <WrapForm
        {...{
          handleSave,
          formCtx,
          formTestID: "register",
        }}
      >
        <BodyFormRegister
          {...{
            swapState,
          }}
        />

        <WrapFormFooter
          {...{
            propsBtnsSwapper: {
              swapState,
              startSwap,
              totSwaps: 2,
            },
            isLoading,
            submitBtnTestID: "register",
          }}
        />
      </WrapForm>
    </WrapFormPage>
  );
};

export default Page;
