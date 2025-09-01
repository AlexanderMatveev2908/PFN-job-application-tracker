/** @jsxImportSource @emotion/react */
"use client";

import { logFormErrs } from "@/core/lib/etc";
import FormResetPwd from "@/core/forms/FormResetPwd/FormResetPwd";
import { usePwdsForm } from "@/core/forms/FormResetPwd/hooks/usePwdsForm";
import { useCallback, type FC } from "react";
import { useUser } from "@/features/user/hooks/useUser";
import { useCheckCbcHmac } from "@/core/hooks/etc/useCheckCbcHmac";
import { TokenT } from "@/common/types/tokens";
import { useRunOnHydrate } from "@/core/hooks/etc/useRunOnHydrate";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { authSliceAPI } from "@/features/auth/slices/api";
import { useManageCbcHmac } from "@/features/user/hooks/useManageCbcHmac";

const Page: FC = () => {
  const { formCtx } = usePwdsForm();
  const { handleSubmit } = formCtx;

  const { userState, loginUser } = useUser();
  const { checkCbcHmac } = useCheckCbcHmac();
  const { nav, wrapAPI } = useKitHooks();
  const { delCbcHmac } = useManageCbcHmac();

  const [mutate, { isLoading }] = authSliceAPI.useRecoverPwdAuthMutation();

  const handleSave = handleSubmit(async (data) => {
    const res = await wrapAPI({
      cbAPI: () =>
        mutate({ ...data, cbc_hmac_token: userState.cbc_hmac_token }),
    });

    if (res.isErr) return;

    if (res.access_token) {
      loginUser(res.access_token);
      delCbcHmac();

      nav.replace("/");
    }
  }, logFormErrs);

  const checkCb = useCallback(() => {
    checkCbcHmac(userState.cbc_hmac_token, TokenT.RECOVER_PWD);
  }, [checkCbcHmac, userState.cbc_hmac_token]);

  useRunOnHydrate({ cb: checkCb });

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
