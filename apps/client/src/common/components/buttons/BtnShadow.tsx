/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import WrapElWithShadow from "../HOC/shapes/WrapElWithShadow";
import { SerializedStyles } from "@emotion/react";
import { FieldTxtSvgT, TestIDT } from "@/common/types/ui";
import { AppEventT } from "@/common/types/api";

type PropsType = {
  handleClick?: () => void;
  $customLabelCSS?: SerializedStyles;
  isEnabled?: boolean;
  isLoading?: boolean;
  el: FieldTxtSvgT;
  act: AppEventT;
} & TestIDT;

const BtnShadow: FC<PropsType> = (arg: PropsType) => {
  return (
    <WrapElWithShadow
      {...{
        ...arg,
        wrapper: "html_button",
      }}
    />
  );
};

export default BtnShadow;
