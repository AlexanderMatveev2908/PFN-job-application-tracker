/** @jsxImportSource @emotion/react */
"use client";

import { UnwrappedResApiT } from "@/common/types/api";
import { TokenT } from "@/common/types/tokens";
import Form2FA from "@/core/forms/Form2FA/Form2FA";
import { use2FAForm } from "@/core/hooks/etc/forms/use2FAForm";
import { useCheckTypeCbcHmac } from "@/core/hooks/etc/tokens/useCheckTypeCbcHmac";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { verifySliceAPI } from "@/features/verify/slices/api";

import { useCallback, type FC } from "react";

const Page: FC = () => {
  const [mutate] = verifySliceAPI.useRecoverPwd2FAMutation();
  const { nav } = useKitHooks();

  const successCb = useCallback(
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    async (_: UnwrappedResApiT<object>) => {
      nav.replace("/auth/recover-password");
    },
    [nav]
  );

  const props = use2FAForm({
    mutationTrigger: mutate,
    successCb,
    delCbcOnSuccess: false,
  });

  useCheckTypeCbcHmac({ tokenType: TokenT.RECOVER_PWD_2FA });

  return <Form2FA {...{ ...props }} />;
};

export default Page;
