/** @jsxImportSource @emotion/react */
"use client";

import { FieldTxtSvgT } from "@/common/types/ui";
import type { FC } from "react";
import SpinTxt from "./elements/spinners/SpinTxt";
import { AppEventT } from "@/common/types/api";

type PropsType = {
  el: FieldTxtSvgT;
  $SvgCls?: string;
  act?: AppEventT;
  isLoading?: boolean;
  isHover?: boolean;
};

const PairTxtSvg: FC<PropsType> = ({
  el,
  $SvgCls,
  isLoading,
  isHover,
  act = "NONE",
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
          <el.Svg className={$SvgCls ?? "svg__md"} />
        ))}

      {el.label && <span className="txt__lg">{el.label}</span>}
    </div>
  );
};

export default PairTxtSvg;
