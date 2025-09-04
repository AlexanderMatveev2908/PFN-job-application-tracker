/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

const WrapPage: FC<ChildrenT> = ({ children }) => {
  return (
    <div className="w-full flex flex-col justify-center gap-10">{children}</div>
  );
};

export default WrapPage;
