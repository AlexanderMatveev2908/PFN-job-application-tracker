/** @jsxImportSource @emotion/react */
"use client";

import WrapFormPage from "@/common/components/forms/shapes/WrapFormPage";
import { useManageCbcHmac } from "@/core/hooks/etc/tokens/useManageCbcHmac";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { useFocus } from "@/core/hooks/ui/useFocus";
import { logFormErrs } from "@/core/lib/etc";
import { PwdFormT, pwdSchema, resetValsPwdForm } from "@/core/paperwork";
import BodyFormAccessManageAccount from "@/features/user/pages/access-manage-account/components/BodyFormAccessManageAccount";
import {
  GainAccessManageAccReturnT,
  userSliceAPI,
} from "@/features/user/slices/api";
import { zodResolver } from "@hookform/resolvers/zod";
import { type FC } from "react";
import { useForm } from "react-hook-form";

const Page: FC = () => {
  const { wrapAPI, nav } = useKitHooks();
  const { saveCbcHmac } = useManageCbcHmac();
  const [mutate, { isLoading }] = userSliceAPI.useGainAccessManageAccMutation();

  const formCtx = useForm<PwdFormT>({
    mode: "onChange",
    resolver: zodResolver(pwdSchema),
    defaultValues: resetValsPwdForm,
  });

  const { handleSubmit, setFocus, reset } = formCtx;

  useFocus("password", { setFocus });

  const handleSave = handleSubmit(async (data) => {
    const res = await wrapAPI<GainAccessManageAccReturnT>({
      cbAPI: () => mutate(data),
    });

    if (res?.isErr) return;

    if (res?.cbc_hmac_token) {
      saveCbcHmac(res.cbc_hmac_token);
      reset(resetValsPwdForm);
      nav.replace("/user/manage-account");
    }
  }, logFormErrs);

  return (
    <WrapFormPage
      {...{
        formCtx,
        formTestID: "manage_acc",
        isLoading,
        handleSave,
      }}
    >
      <BodyFormAccessManageAccount />
    </WrapFormPage>
  );
};

export default Page;
