/** @jsxImportSource @emotion/react */
"use client";

import { UnwrappedResApiT } from "@/common/types/api";
import Form2FA from "@/core/forms/Form2FA/Form2FA";
import { use2FAForm } from "@/core/hooks/etc/forms/use2FAForm";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { AccessTokenReturnT, authSliceAPI } from "@/features/auth/slices/api";
import { useUser } from "@/features/user/hooks/useUser";
import { useCallback, type FC } from "react";

const Page: FC = () => {
  const [mutate] = authSliceAPI.useLoginAuth2FAMutation();
  const { nav } = useKitHooks();
  const { loginUser } = useUser();

  const successCb = useCallback(
    async (res: UnwrappedResApiT<AccessTokenReturnT>) => {
      if (!res.access_token) return;

      loginUser(res.access_token);

      nav.replace("/");
    },
    [loginUser, nav]
  );

  const props = use2FAForm({
    mutationTrigger: mutate,
    successCb,
  });

  return <Form2FA {...{ ...props }} />;
};

export default Page;
