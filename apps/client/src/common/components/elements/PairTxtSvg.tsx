/** @jsxImportSource @emotion/react */
"use client";

import { FieldTxtSvgT } from "@/common/types/ui";
import type { FC } from "react";

type PropsType = {
  el: FieldTxtSvgT;
  $SvgCls?: string;
};

const PairTxtSvg: FC<PropsType> = ({ el, $SvgCls }) => {
  return (
    <div className="flex items-center justify-start gap-6">
      {el.Svg && <el.Svg className={$SvgCls ?? "svg__md"} />}

      {el.label && <span className="txt__lg">{el.label}</span>}
    </div>
  );
};

export default PairTxtSvg;
