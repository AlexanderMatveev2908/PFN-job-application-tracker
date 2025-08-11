/** @jsxImportSource @emotion/react */
"use client";

import SvgPasswordCursor from "@/common/components/SVGs/PasswordCursor";
import type { FC } from "react";
import BtnSvg from "@/common/components/buttons/BtnSvg";
import { SwapModeT } from "@/app/auth/register/page";

type PropsType = {
  swapMode?: SwapModeT;
  isCurrSwap?: boolean;
};

const PwdGenerator: FC<PropsType> = ({
  swapMode = "swapped",
  isCurrSwap = true,
}) => {
  return (
    <div className="w-full grid grid-cols-1">
      <div className="w-fit relative">
        <BtnSvg
          {...{
            Svg: SvgPasswordCursor,
            handleClick: () => null,
            confPortal: {
              optDep: [swapMode],
              showPortal: swapMode === "swapped" && isCurrSwap,
              txt: "Generate Password",
            },
          }}
        />
      </div>
    </div>
  );
};

export default PwdGenerator;
