"use client";

import { useEndPendingActionUser } from "@/features/user/hooks/useEndPendingActionUser";
import { FC } from "react";

const Page: FC = () => {
  useEndPendingActionUser();

  return <div></div>;
};

export default Page;
