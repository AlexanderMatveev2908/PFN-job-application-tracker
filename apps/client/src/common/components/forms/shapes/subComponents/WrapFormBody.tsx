/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

const WrapFormBody: FC<ChildrenT> = ({ children }) => {
  return (
    <div className="grid grid-cols-1 gap-6 w-full h-fit items-start p-5">
      {children}
    </div>
  );
};

export default WrapFormBody;
