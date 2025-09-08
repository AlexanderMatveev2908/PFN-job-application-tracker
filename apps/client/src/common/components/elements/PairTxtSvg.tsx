/** @jsxImportSource @emotion/react */
"use client";

import { FieldTxtSvgT } from "@/common/types/ui";
import type { FC } from "react";
import SpinTxt from "./spinners/SpinTxt";
import { AppEventT } from "@/common/types/api";
import { css, SerializedStyles } from "@emotion/react";

type PropsType = {
  el: FieldTxtSvgT;
  act?: AppEventT;
  isLoading?: boolean;
  isHover?: boolean;
  $SvgCls?: string;
  $ctmLabelCSS?: SerializedStyles;
};

const PairTxtSvg: FC<PropsType> = ({
  el,
  $SvgCls,
  isLoading,
  isHover,
  act = "NONE",
  $ctmLabelCSS,
}) => {
  return (
    <div className="flex items-center justify-start gap-6">
      {el.Svg &&
        (isLoading ? (
          <SpinTxt
            {...{
              act,
              isHover,
            }}
          />
        ) : (
          <el.Svg className={$SvgCls ?? "svg__sm"} />
        ))}

      {el.label && (
        <span
          className="txt__lg"
          css={css`
            ${$ctmLabelCSS}
          `}
        >
          {el.label}
        </span>
      )}
    </div>
  );
};

export default PairTxtSvg;
