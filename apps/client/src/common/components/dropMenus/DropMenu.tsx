/** @jsxImportSource @emotion/react */
"use client";

import { DropElT } from "@/common/types/ui";
import type { FC } from "react";
import SvgDown from "../SVGs/Down";

type PropsType = {
  el: DropElT;
};

const DropMenu: FC<PropsType> = ({ el }) => {
  return (
    <div className="w-full flex flex-col">
      <div className="flex items-center justify-start gap-6">
        {el.Svg && <el.Svg className="svg__md txt__clr" />}

        <span className="txt__md">{el.label}</span>
      </div>

      <SvgDown className="svg__md txt__clr" />
    </div>
  );
};

export default DropMenu;
