/** @jsxImportSource @emotion/react */
"use client";

import WrapFormPage from "@/common/components/forms/shapes/WrapFormPage";
import { useFocus } from "@/core/hooks/ui/useFocus";
import { logFormErrs } from "@/core/lib/etc";
import { __cg } from "@/core/lib/log";
import { PwdFormT, pwdSchema, resetValsPwdForm } from "@/core/paperwork";
import BodyFormAccessManageAccount from "@/features/user/pages/access-manage-account/components/BodyFormAccessManageAccount";
import { zodResolver } from "@hookform/resolvers/zod";
import type { FC } from "react";
import { useForm } from "react-hook-form";

const Page: FC = () => {
  const formCtx = useForm<PwdFormT>({
    mode: "onChange",
    resolver: zodResolver(pwdSchema),
    defaultValues: resetValsPwdForm,
  });

  const { handleSubmit, setFocus } = formCtx;

  useFocus("password", { setFocus });

  const handleSave = handleSubmit(async (data) => {
    __cg(data);
  }, logFormErrs);

  return (
    <WrapFormPage
      {...{
        formCtx,
        formTestID: "manage_acc",
        isLoading: false,
        handleSave,
      }}
    >
      <BodyFormAccessManageAccount />
    </WrapFormPage>
  );
};

export default Page;
