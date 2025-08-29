/** @jsxImportSource @emotion/react */
"use client";

import { useWrapQuery } from "@/core/hooks/api/useWrapQuery";
import { testSliceAPI } from "@/features/test/slices/api";
import type { FC } from "react";

const Page: FC = () => {
  const res = testSliceAPI.useGetProtectedQuery();
  useWrapQuery(res);

  return <div></div>;
};

export default Page;
