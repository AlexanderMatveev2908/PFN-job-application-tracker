/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import WrapShadow from "../HOC/buttonWrappers/WrapShadow";
import { SerializedStyles } from "@emotion/react";
import { FieldTxtSvgT } from "@/common/types/ui";
import { AppEventT } from "@/common/types/api";

type PropsType = {
  handleClick?: () => void;
  $customLabelCSS?: SerializedStyles;
  isEnabled?: boolean;
  isLoading?: boolean;
  el: FieldTxtSvgT;
  act: AppEventT;
};

const BtnShadow: FC<PropsType> = (arg: PropsType) => {
  return (
    <WrapShadow
      {...{
        ...arg,
        wrapper: "html_button",
      }}
    />
  );
};

export default BtnShadow;
