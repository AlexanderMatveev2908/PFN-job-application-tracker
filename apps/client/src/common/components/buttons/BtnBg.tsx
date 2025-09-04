/** @jsxImportSource @emotion/react */
"use client";

import { type CSSProperties, type FC } from "react";
import PairTxtSvg from "../elements/PairTxtSvg";
import { FieldTxtSvgT } from "@/common/types/ui";
import { AppEventT } from "@/common/types/api";
import { $argClr } from "@/core/uiFactory/style";
import { css } from "@emotion/react";

type PropsType = {
  el: FieldTxtSvgT;
  act?: AppEventT;
  $fill?: string;
};

const BtnBg: FC<PropsType> = ({ el, act = "NONE", $fill }) => {
  const $clr = $argClr[act];

  return (
    <button
      type="button"
      className="btn__sm btn__app flex items-center justify-center w-full py-2 px-4"
      style={
        {
          "--scale__up": 1.15,
        } as CSSProperties
      }
      css={css`
        color: ${$clr};
        border-color: ${$clr};

        &:enabled:hover {
          background: ${$clr};
          color: var(--${act === "NONE" ? "neutral__950" : "white__0"});
          fill: ${$fill};
        }
      `}
    >
      <PairTxtSvg
        {...{
          el,
        }}
      />
    </button>
  );
};

export default BtnBg;
