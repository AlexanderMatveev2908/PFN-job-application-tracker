/** @jsxImportSource @emotion/react */
"use client";

import { type FC } from "react";
import WrapSvgTooltip, { WrapSvgTltPropsT } from "../HOC/shapes/WrapSvgTooltip";

type PropsType = {
  handleClick: () => void;
  isEnabled?: boolean;
} & WrapSvgTltPropsT;

const BtnSvg: FC<PropsType> = ({
  handleClick,
  act = "NONE",
  Svg,
  isEnabled = true,
  confPortal,
}) => {
  return (
    <WrapSvgTooltip
      {...{
        wrapper: "html_button",
        propsBtn: {
          handleClick,
          isEnabled,
        },
        confPortal,
        act,
        Svg,
      }}
    />
  );
};

export default BtnSvg;
