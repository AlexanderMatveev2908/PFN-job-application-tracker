/** @jsxImportSource @emotion/react */
"use client";

import { type FC } from "react";
import WrapSvgTooltip, { WrapSvgTltPropsT } from "../HOC/shapes/WrapSvgTooltip";
import { TestIdT } from "@/common/types/ui";

type PropsType = {
  handleClick: () => void;
  isEnabled?: boolean;
} & WrapSvgTltPropsT &
  TestIdT;

const BtnSvg: FC<PropsType> = ({
  handleClick,
  act = "NONE",
  Svg,
  isEnabled = true,
  confPortal,
  t_id,
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
        t_id,
      }}
    />
  );
};

export default BtnSvg;
