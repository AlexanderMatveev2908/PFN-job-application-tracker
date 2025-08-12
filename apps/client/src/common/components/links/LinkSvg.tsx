/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import WrapSvgTooltip, { WrapSvgTltPropsT } from "../HOC/shapes/WrapSvgTooltip";

type PropsType = {
  href: string;
} & WrapSvgTltPropsT;

const LinkSvg: FC<PropsType> = ({ Svg, act, confPortal, href }) => {
  return (
    <WrapSvgTooltip
      {...{
        wrapper: "next_link",
        Svg,
        act,
        confPortal,
        propsLink: {
          href,
        },
      }}
    />
  );
};

export default LinkSvg;
