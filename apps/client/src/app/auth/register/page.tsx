"use client";

import Register from "@/features/auth/pages/register/Register";
import { FC } from "react";

const Page: FC = () => {
  return (
    <div className="auth__form">
      <Register />
    </div>
  );
};

export default Page;
