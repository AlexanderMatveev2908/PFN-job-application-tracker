/** @jsxImportSource @emotion/react */
"use client";

import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import WrapSwap, {
  PropsTypeWrapSwap,
} from "@/common/components/swap/subComponents/WrapSwap";
import {
  EmailFormT,
  resetValsEmailForm,
} from "@/core/forms/RequireEmailForm/paperwork";
import { emailField } from "@/core/forms/RequireEmailForm/uiFactory";
import { SwapStateT } from "@/core/hooks/etc/useSwap/etc/initState";
import { emailSchema } from "@/core/paperwork";
import { useGetUserState } from "@/features/user/hooks/useGetUserState";
import { zodResolver } from "@hookform/resolvers/zod";
import type { FC } from "react";
import { useForm } from "react-hook-form";

type PropsType = {
  swapState: SwapStateT;
} & Omit<PropsTypeWrapSwap, "children">;

const ChangeEmailForm: FC<PropsType> = ({ contentRef, isCurr, swapState }) => {
  const { user } = useGetUserState();
  const { swapMode, currSwap } = swapState;

  const schemaX = emailSchema.refine((data) => data.email !== user?.email, {
    message: "new email must be different from old one",
    path: ["email"],
  });

  const formCtx = useForm<EmailFormT>({
    mode: "onChange",
    resolver: zodResolver(schemaX),
    defaultValues: resetValsEmailForm,
  });

  const { control } = formCtx;

  return (
    <WrapSwap
      {...{
        contentRef,
        isCurr,
      }}
    >
      <FormFieldTxt
        {...{
          el: emailField,
          control,
          portalConf: {
            showPortal: isCurr && swapMode !== "swapping",
            optDep: [currSwap],
          },
        }}
      />
    </WrapSwap>
  );
};

export default ChangeEmailForm;
