import { useForm } from "react-hook-form";
import { useListenHeight } from "../height/useListenHeight";
import { useSwap } from "../useSwap/useSwap";
import {
  BackupCodeFormT,
  resetValsBackupForm,
  resetValsTotpForm,
  schemaBackupForm,
  schemaTotpCode,
  ToptFormT,
} from "@/core/paperwork";
import { zodResolver } from "@hookform/resolvers/zod";
import { logFormErrs } from "@/core/lib/etc";
import { useUser } from "@/features/user/hooks/useUser";
import { useCallback } from "react";
import { useKitHooks } from "../useKitHooks";
import { DataApiT } from "@/common/types/api";
import { useManageCbcHmac } from "../tokens/useManageCbcHmac";

type Params = {
  mutationTrigger: (args: {
    cbc_hmac_token: string;
    totp_code?: string;
    backup_code?: string;
  }) => {
    unwrap: () => Promise<{
      data: DataApiT;
    }>;
  };
  successCb: () => void;
};

export const use2FAForm = ({ mutationTrigger, successCb }: Params) => {
  const { startSwap, swapState } = useSwap();
  const { currSwap } = swapState;

  const { userState } = useUser();
  const { wrapAPI } = useKitHooks();
  const { delCbcHmac } = useManageCbcHmac();

  const mainCb = useCallback(
    async ({
      totp_code,
      backup_code,
    }: {
      totp_code?: string;
      backup_code?: string;
    }) => {
      const res = await wrapAPI({
        cbAPI: () =>
          mutationTrigger({
            cbc_hmac_token: userState.cbc_hmac_token,
            ...(totp_code ? { totp_code } : { backup_code }),
          }),
        pushNotice: [401],
      });

      if (!res) return;

      delCbcHmac();

      successCb();
    },
    [userState.cbc_hmac_token, wrapAPI, delCbcHmac, mutationTrigger, successCb]
  );

  const { contentRef, contentH } = useListenHeight({
    opdDep: [currSwap],
  });

  const formBackupCodeCtx = useForm<BackupCodeFormT>({
    mode: "onChange",
    resolver: zodResolver(schemaBackupForm),
    defaultValues: resetValsBackupForm,
  });

  const { handleSubmit: submitBackupCode } = formBackupCodeCtx;

  const handleSaveBackupCode = submitBackupCode(async (data) => {
    await mainCb({
      backup_code: data.backup_code,
    });
  }, logFormErrs);

  const formTotpCtx = useForm<ToptFormT>({
    mode: "onChange",
    resolver: zodResolver(schemaTotpCode),
    defaultValues: resetValsTotpForm,
  });

  const { handleSubmit: submitTotp } = formTotpCtx;

  const handleSaveTotp = submitTotp(async (data) => {
    await mainCb({
      totp_code: data.totp_code.join(""),
    });
  }, logFormErrs);

  return {
    startSwap,
    swapState,
    contentRef,
    contentH,
    totpProps: {
      formCtx: formTotpCtx,
      handleSave: handleSaveTotp,
    },
    backupCodeProps: {
      formCtx: formBackupCodeCtx,
      handleSave: handleSaveBackupCode,
    },
  };
};
