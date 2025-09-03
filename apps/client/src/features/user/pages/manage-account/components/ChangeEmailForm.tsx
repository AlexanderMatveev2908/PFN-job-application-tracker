/** @jsxImportSource @emotion/react */
"use client";

import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import { PropsTypeWrapSwap } from "@/common/components/swap/subComponents/WrapSwap";
import { genMailNoticeMsg } from "@/core/constants/etc";
import {
  EmailFormT,
  resetValsEmailForm,
} from "@/core/forms/RequireEmailForm/paperwork";
import { emailField } from "@/core/forms/RequireEmailForm/uiFactory";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { SwapStateT } from "@/core/hooks/etc/useSwap/etc/initState";
import { logFormErrs } from "@/core/lib/etc";
import { emailSchema } from "@/core/paperwork";
import WrapFormManageAcc from "@/features/user/components/WrapFormManageAcc";
import { useGetUserState } from "@/features/user/hooks/useGetUserState";
import { userSliceAPI } from "@/features/user/slices/api";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, type FC } from "react";
import { useForm } from "react-hook-form";

type PropsType = {
  swapState: SwapStateT;
} & Omit<PropsTypeWrapSwap, "children">;

const ChangeEmailForm: FC<PropsType> = ({ contentRef, isCurr, swapState }) => {
  const { user } = useGetUserState();
  const { swapMode, currSwap } = swapState;

  const schemaX = emailSchema.refine((data) => data.email !== user?.email, {
    message: "new email must be different from old one",
    path: ["email"],
  });

  const formCtx = useForm<EmailFormT>({
    mode: "onChange",
    resolver: zodResolver(schemaX),
    defaultValues: resetValsEmailForm,
  });
  const { handleSubmit, setFocus, reset } = formCtx;

  const [mutate, { isLoading }] = userSliceAPI.useChangeEmailMutation();
  const { cbc_hmac_token } = useGetUserState();
  const { setNotice, wrapAPI, nav } = useKitHooks();

  const handleSave = handleSubmit(async (data) => {
    const res = await wrapAPI<void>({
      cbAPI: () =>
        mutate({
          ...data,
          cbc_hmac_token,
        }),
      pushNotice: true,
    });

    if (!res) return;

    setNotice({
      msg: genMailNoticeMsg("to change your account email"),
      type: "OK",
      child: "OPEN_MAIL_APP",
    });

    reset(resetValsEmailForm);

    nav.replace("/notice");
  }, logFormErrs);

  const { control } = formCtx;

  const isFixedOnCurrForm = isCurr && swapMode !== "swapping";

  useEffect(() => {
    if (isFixedOnCurrForm) setFocus("email");
  }, [setFocus, isFixedOnCurrForm]);

  return (
    <WrapFormManageAcc
      {...{
        contentRef,
        isCurr,
        title: "Change Email",
        handleSave,
        formCtx,
        isLoading,
      }}
    >
      <FormFieldTxt
        {...{
          el: emailField,
          control,
          portalConf: {
            showPortal: isFixedOnCurrForm,
            optDep: [currSwap],
          },
        }}
      />
    </WrapFormManageAcc>
  );
};

export default ChangeEmailForm;
