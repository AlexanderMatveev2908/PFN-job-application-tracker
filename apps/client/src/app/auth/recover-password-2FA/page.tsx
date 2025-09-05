/** @jsxImportSource @emotion/react */
"use client";

import { TokenT } from "@/common/types/tokens";
import FormResetPwd from "@/core/forms/FormResetPwd/FormResetPwd";
import { usePwdsForm } from "@/core/hooks/etc/forms/usePwdsForm";
import { useCheckTypeCbcHmac } from "@/core/hooks/etc/tokens/useCheckTypeCbcHmac";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { logFormErrs } from "@/core/lib/etc";
import { authSliceAPI } from "@/features/auth/slices/api";
import { useUser } from "@/features/user/hooks/useUser";
import type { FC } from "react";

const Page: FC = () => {
  const { formCtx } = usePwdsForm();
  const { handleSubmit } = formCtx;

  const { userState, loginUser, delCbcHmac } = useUser();
  const { nav, wrapAPI } = useKitHooks();

  const [mutate, { isLoading }] =
    authSliceAPI.useRecoverPwdAuthReset2FAMutation();

  const handleSave = handleSubmit(async (data) => {
    const res = await wrapAPI({
      cbAPI: () =>
        mutate({ ...data, cbc_hmac_token: userState.cbc_hmac_token }),
    });

    if (!res) return;

    if (res?.access_token) {
      loginUser(res.access_token);
      delCbcHmac();

      nav.replace("/");
    }
  }, logFormErrs);

  useCheckTypeCbcHmac({ tokenType: TokenT.RECOVER_PWD_2FA });

  return (
    <FormResetPwd
      {...{
        handleSave,
        formCtx,
        testID: "recover_pwd",
        isLoading,
      }}
    />
  );
};

export default Page;
