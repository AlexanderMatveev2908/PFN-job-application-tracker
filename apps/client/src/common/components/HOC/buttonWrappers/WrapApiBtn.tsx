/** @jsxImportSource @emotion/react */
"use client";

import type { FC, ReactNode } from "react";
import SpinBtn from "../../spinners/SpinBtn";
import { AppEventT } from "@/common/types/api";

type PropsType = {
  isLoading?: boolean;
  act?: AppEventT;
  children: ReactNode;
};

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
