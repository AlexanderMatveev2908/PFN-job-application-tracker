/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import WrapElWithShadow from "../HOC/shapes/WrapElWithShadow";
import { SerializedStyles } from "@emotion/react";
import { FieldTxtSvgT } from "@/common/types/ui";
import { AppEventT } from "@/common/types/api";

type PropsType = {
  handleClick?: () => void;
  href: string;
  download?: string;
  $customLabelCSS?: SerializedStyles;
  el: FieldTxtSvgT;
  act: AppEventT;
};
const LinkShadow: FC<PropsType> = (arg: PropsType) => {
  return (
    <WrapElWithShadow
      {...{
        ...arg,
        wrapper: "next_link",
      }}
    />
  );
};

export default LinkShadow;
