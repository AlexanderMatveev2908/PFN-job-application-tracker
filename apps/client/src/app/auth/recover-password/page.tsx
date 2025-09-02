/** @jsxImportSource @emotion/react */
"use client";

import { logFormErrs } from "@/core/lib/etc";
import FormResetPwd from "@/core/forms/FormResetPwd/FormResetPwd";
import { usePwdsForm } from "@/core/forms/FormResetPwd/hooks/usePwdsForm";
import { type FC } from "react";
import { useUser } from "@/features/user/hooks/useUser";
import { TokenT } from "@/common/types/tokens";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { authSliceAPI } from "@/features/auth/slices/api";
import { useManageCbcHmac } from "@/features/user/hooks/useManageCbcHmac";
import { useCheckTypeCbcHmac } from "@/core/hooks/etc/tokens/useCheckTypeCbcHmac";

const Page: FC = () => {
  const { formCtx } = usePwdsForm();
  const { handleSubmit } = formCtx;

  const { userState, loginUser } = useUser();
  const { nav, wrapAPI } = useKitHooks();
  const { delCbcHmac } = useManageCbcHmac();

  const [mutate, { isLoading }] = authSliceAPI.useRecoverPwdAuthMutation();

  const handleSave = handleSubmit(async (data) => {
    const res = await wrapAPI({
      cbAPI: () =>
        mutate({ ...data, cbc_hmac_token: userState.cbc_hmac_token }),
    });

    if (res?.isErr) return;

    if (res?.access_token) {
      loginUser(res.access_token);
      delCbcHmac();

      nav.replace("/");
    }
  }, logFormErrs);

  useCheckTypeCbcHmac({ tokenType: TokenT.RECOVER_PWD });

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
