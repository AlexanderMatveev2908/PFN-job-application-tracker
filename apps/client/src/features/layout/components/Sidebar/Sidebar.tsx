/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { css } from "@emotion/react";
import { headerHight } from "@/core/constants/style";
import { useSelector } from "react-redux";
import { getSideState } from "./slice";
import { __cg } from "@/core/lib/log";

const Sidebar: FC = () => {
  const sideState = useSelector(getSideState);

  __cg(sideState);

  return (
    <div
      className="fixed h-full border-l-3 border-w_0 right-0 w-[80vw] sm:w-[500px] md:w-[600px]"
      css={css`
        top: ${headerHight}px;
      `}
    ></div>
  );
};

export default Sidebar;
