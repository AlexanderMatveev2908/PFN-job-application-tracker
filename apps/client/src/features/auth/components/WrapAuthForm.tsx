/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

const WrapAuthForm: FC<ChildrenT> = ({ children }) => {
  return (
    <div className="w-full mx-auto mt-[50px] max-w-[800px] h-fit bd__md rounded-xl p-5 sm:p-8 pb-8 sm:pb-12 overflow-hidden">
      {children}
    </div>
  );
};

export default WrapAuthForm;
