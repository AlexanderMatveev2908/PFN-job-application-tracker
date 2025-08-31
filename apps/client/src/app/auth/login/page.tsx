"use client";

import AuthPageWrap from "@/features/auth/components/AuthPageWrap";
import { useEndPendingActionUser } from "@/features/user/hooks/useEndPendingActionUser";
import { FC } from "react";

const Page: FC = () => {
  useEndPendingActionUser();

  return (
    <AuthPageWrap>
      <div className=""></div>
    </AuthPageWrap>
  );
};

export default Page;
