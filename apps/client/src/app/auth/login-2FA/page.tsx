/** @jsxImportSource @emotion/react */
"use client";

import Form2FA from "@/core/forms/Form2FA/Form2FA";
import { use2FAForm } from "@/core/hooks/etc/forms/use2FAForm";
import type { FC } from "react";

const Page: FC = () => {
  const props = use2FAForm({});

  return <Form2FA {...props} />;
};

export default Page;
