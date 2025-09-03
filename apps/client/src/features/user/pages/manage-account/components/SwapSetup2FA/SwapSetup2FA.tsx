/** @jsxImportSource @emotion/react */
"use client";

import { useState, type FC } from "react";
import WrapSwapManageAcc from "../subComponents/WrapSwapManageAcc";
import { FormManageAccPropsType } from "../../types";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { useGetUserState } from "@/features/user/hooks/useGetUserState";
import { Setup2FAReturnT, userSliceAPI } from "@/features/user/slices/api";
import { UserT } from "@/features/user/types";
import ContentSetup2FA from "./components/ContentSetup2FA";
import NoticeSetup2FA from "./components/NoticeSetup2FA";

const SwapSetup2FA: FC<FormManageAccPropsType & { user: UserT | null }> = ({
  contentRef,
  isCurr,
  swapState,
  user,
}) => {
  const [res2FA, setRes2FA] = useState<Setup2FAReturnT | null>(null);

  const testID = "setup_2FA";

  const [mutate, { isLoading }] = userSliceAPI.useSetup2FAMutation();

  const { wrapAPI } = useKitHooks();
  const { cbc_hmac_token } = useGetUserState();

  const handleClick = async () => {
    const res = await wrapAPI<Setup2FAReturnT>({
      cbAPI: () => mutate({ cbc_hmac_token }),
      pushNotice: [401],
    });

    if (!res) return;

    setRes2FA({
      totp_secret_qrcode: res.totp_secret_qrcode,
      totp_secret: res.totp_secret,
      backup_codes: res.backup_codes,
      zip_file: res.zip_file,
    });
  };

  return (
    <WrapSwapManageAcc
      {...{
        contentRef,
        isCurr,
        title: "Setup 2FA",
        testID,
      }}
    >
      {!res2FA && (user?.use_2FA || !user?.is_verified) ? (
        <NoticeSetup2FA
          {...{
            user,
          }}
        />
      ) : (
        <ContentSetup2FA
          {...{
            handleClick,
            isCurr,
            isLoading,
            res2FA,
            swapState,
            testID,
            contentRef,
          }}
        />
      )}
    </WrapSwapManageAcc>
  );
};

export default SwapSetup2FA;
