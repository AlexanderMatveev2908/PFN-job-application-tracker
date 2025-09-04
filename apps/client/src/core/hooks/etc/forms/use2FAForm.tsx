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
import { __cg } from "@/core/lib/log";
import { logFormErrs } from "@/core/lib/etc";
import { Form2FAPropsType } from "@/core/forms/Form2FA/Form2FA";

type Params = object;

export const use2FAForm = ({}: Params): Form2FAPropsType => {
  const { startSwap, swapState } = useSwap();
  const { currSwap } = swapState;

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
    __cg(data);
  }, logFormErrs);

  const formTotpCtx = useForm<ToptFormT>({
    mode: "onChange",
    resolver: zodResolver(schemaTotpCode),
    defaultValues: resetValsTotpForm,
  });

  const { handleSubmit: submitTotp } = formTotpCtx;

  const handleSaveTotp = submitTotp(async (data) => {
    __cg(data);
  }, logFormErrs);

  return {
    startSwap,
    swapState,
    contentRef,
    contentH,
    totpProps: {
      handleSave: handleSaveBackupCode,
      formCtx: formBackupCodeCtx,
    },
    backupCodeProps: {
      handleSave: handleSaveTotp,
      formCtx: formTotpCtx,
    },
  };
};
