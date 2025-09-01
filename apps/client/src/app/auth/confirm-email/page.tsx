"use client";

import { genMailNoticeMsg } from "@/core/constants/etc";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { logFormErrs } from "@/core/lib/etc";
import RequireEmailForm from "@/features/requireEmail/components/RequireEmailForm/AuthEmailForm";
import { useEmailForm } from "@/features/requireEmail/components/RequireEmailForm/hooks/useEmailForm";
import { resetValsEmailForm } from "@/features/requireEmail/components/RequireEmailForm/paperwork";
import { requireEmailSliceAPI } from "@/features/requireEmail/slices/api";
import type { FC } from "react";

const Page: FC = () => {
  const { formCtx } = useEmailForm();
  const { handleSubmit, reset } = formCtx;

  const { wrapAPI, setNotice, nav } = useKitHooks();
  const [mutate, { isLoading }] =
    requireEmailSliceAPI.useRequireConfEmailMutation();

  const handleSave = handleSubmit(async (data) => {
    const res = await wrapAPI<void>({
      cbAPI: () => mutate(data),
    });

    if (res.isErr) return;

    reset(resetValsEmailForm);

    setNotice({
      msg: genMailNoticeMsg("to confirm the account"),
      type: "OK",
      child: "OPEN_MAIL_APP",
    });

    nav.replace("/notice");
  }, logFormErrs);

  return (
    <RequireEmailForm
      {...{
        formCtx,
        testID: "conf_email",
        isLoading,
        handleSave,
      }}
    />
  );
};

export default Page;
