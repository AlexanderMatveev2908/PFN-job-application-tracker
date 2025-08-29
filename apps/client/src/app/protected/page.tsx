/** @jsxImportSource @emotion/react */
"use client";

import { useWrapQuery } from "@/core/hooks/api/useWrapQuery";
import { testSliceAPI } from "@/features/test/slices/api";
import { useGetUsState } from "@/features/user/hooks/useGetUsState";
import { useRouter } from "next/navigation";
import { useEffect, type FC } from "react";

const Page: FC = () => {
  const canBePushed = useGetUsState().canBePushed;

  const nav = useRouter();

  const res = testSliceAPI.useGetProtectedQuery();
  useWrapQuery(res);

  // useEffect(() => {
  //   if (canBePushed) nav.replace("/auth/login");
  // }, [canBePushed, nav]);

  return <div></div>;
};

export default Page;
