/** @jsxImportSource @emotion/react */
"use client";

import { AppEventT } from "@/common/types/api";
import { type FC } from "react";
import { IconType } from "react-icons";
import { PortalConfT } from "@/common/types/ui";
import WrapSvgTooltip from "../HOC/shapes/WrapSvgTooltip";

type PropsType = {
  handleClick: () => void;
  Svg: IconType;
  act?: AppEventT;
  isEnabled?: boolean;
  confPortal?: PortalConfT & { txt: string };
};

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
