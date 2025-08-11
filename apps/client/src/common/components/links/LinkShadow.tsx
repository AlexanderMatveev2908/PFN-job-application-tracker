/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import WrapShadow from "../HOC/buttonWrappers/WrapShadow";
import { SerializedStyles } from "@emotion/react";
import { FieldTxtSvgT } from "@/common/types/ui";
import { AppEventT } from "@/common/types/api";

type PropsType = {
  handleClick?: () => void;
  href?: string;
  $customLabelCSS?: SerializedStyles;
  el: FieldTxtSvgT;
  act: AppEventT;
};
const LinkShadow: FC<PropsType> = (arg: PropsType) => {
  return (
    <WrapShadow
      {...{
        ...arg,
        wrapper: "next_link",
      }}
    />
  );
};

export default LinkShadow;
