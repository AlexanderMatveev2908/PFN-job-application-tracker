/** @jsxImportSource @emotion/react */
"use client";

import Form2FA from "@/core/forms/Form2FA/Form2FA";
import { use2FAForm } from "@/core/hooks/etc/forms/use2FAForm";
import { testSliceAPI } from "@/features/test/slices/api";
import type { FC } from "react";

const Page: FC = () => {
  const [mutate] = testSliceAPI.usePostHelloMutation();

  const props = use2FAForm({
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    mutationTrigger: mutate as any,
    successCb: () => console.log("ok"),
  });

  return <Form2FA {...{ ...props }} />;
};

export default Page;
