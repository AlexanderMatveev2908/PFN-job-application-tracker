/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import SpinBtn from "../../spinners/SpinBtn";
import { AppEventT } from "@/common/types/api";
import { ChildrenT } from "@/common/types/ui";

type PropsType = {
  isLoading?: boolean;
  act?: AppEventT;
} & ChildrenT;

const WrapApiBtn: FC<PropsType> = ({ isLoading, act = "NONE", children }) => {
  return isLoading ? (
    <div className="w-full flex justify-center">
      <SpinBtn {...{ act }} />
    </div>
  ) : (
    children
  );
};

export default WrapApiBtn;
