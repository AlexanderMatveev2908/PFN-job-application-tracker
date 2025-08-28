/** @jsxImportSource @emotion/react */
"use client";

import { genLorem } from "@/core/lib/etc";
import type { FC } from "react";

const Page: FC = () => {
  return <div>{genLorem(10)}</div>;
};

export default Page;
