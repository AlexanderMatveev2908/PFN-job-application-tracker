"use client";

import WrapAuthForm from "@/features/auth/components/WrapAuthForm";
import Register from "@/features/auth/pages/register/Register";
import { FC } from "react";

const Page: FC = () => {
  return (
    <WrapAuthForm>
      <Register />
    </WrapAuthForm>
  );
};

export default Page;
