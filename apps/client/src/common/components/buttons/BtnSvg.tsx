/** @jsxImportSource @emotion/react */
"use client";

import { type FC } from "react";
import WrapElWithSvgTooltip, {
  WrapSvgTltPropsT,
} from "../HOC/shapes/WrapElWithSvgTooltip";
import { TestIDT } from "@/common/types/ui";

type PropsType = {
  handleClick: () => void;
  isEnabled?: boolean;
} & WrapSvgTltPropsT &
  TestIDT;

const BtnSvg: FC<PropsType> = ({
  handleClick,
  act = "NONE",
  Svg,
  isEnabled = true,
  confPortal,
  testID,
}) => {
  return (
    <WrapElWithSvgTooltip
      {...{
        wrapper: "html_button",
        propsBtn: {
          handleClick,
          isEnabled,
        },
        confPortal,
        act,
        Svg,
        testID,
      }}
    />
  );
};

export default BtnSvg;
