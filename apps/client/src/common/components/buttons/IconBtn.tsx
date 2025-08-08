/** @jsxImportSource @emotion/react */
"use client";

import { AppEventT } from "@/common/types/api";
import { css } from "@emotion/react";
import type { FC } from "react";
import { $argClr } from "@/core/uiFactory/style";
import { IconType } from "react-icons";

type PropsType = {
  handleClick: () => void;
  Svg: IconType;
  act?: AppEventT;
  isEnabled?: boolean;
};

const IconBtn: FC<PropsType> = ({
  handleClick,
  act = "NONE",
  Svg,
  isEnabled = true,
}) => {
  const $clr = $argClr[act];

  return (
    <button
      type="button"
      onClick={handleClick}
      disabled={!isEnabled}
      className="btn__app"
      css={css`
        color: ${$clr};
      `}
      style={
        {
          "--scale__up": 1.3,
        } as React.CSSProperties
      }
    >
      <Svg className="svg__lg" />
    </button>
  );
};

export default IconBtn;
