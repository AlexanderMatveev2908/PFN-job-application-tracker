/** @jsxImportSource @emotion/react */
"use client";

import { logFormErrs } from "@/core/lib/etc";
import { __cg } from "@/core/lib/log";
import FormResetPwd from "@/core/forms/FormResetPwd/FormResetPwd";
import { usePwdsForm } from "@/core/forms/FormResetPwd/hooks/usePwdsForm";
import { useCallback, type FC } from "react";
import { useUser } from "@/features/user/hooks/useUser";
import { useCheckCbcHmac } from "@/core/hooks/etc/useCheckCbcHmac";
import { TokenT } from "@/common/types/tokens";
import { useRunOnHydrate } from "@/core/hooks/etc/useRunOnHydrate";

const Page: FC = () => {
  const { formCtx } = usePwdsForm();
  const { handleSubmit } = formCtx;

  const handleSave = handleSubmit(async (data) => {
    __cg(data);
  }, logFormErrs);

  const { userState } = useUser();
  const { checkCbcHmac } = useCheckCbcHmac();

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
        isLoading: false,
      }}
    />
  );
};

export default Page;
