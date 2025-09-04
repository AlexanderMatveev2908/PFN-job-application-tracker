/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

const WrapFormBody: FC<ChildrenT> = ({ children }) => {
  return <div className="form__body">{children}</div>;
};

export default WrapFormBody;
