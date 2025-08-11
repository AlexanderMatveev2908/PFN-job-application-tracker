/** @jsxImportSource @emotion/react */
"use client";

import SvgPasswordCursor from "@/common/components/SVGs/PasswordCursor";
import { useState, type FC } from "react";
import BtnSvg from "@/common/components/buttons/BtnSvg";
import { SwapModeT } from "@/app/auth/register/page";
import CpyPaste from "@/common/components/elements/CpyPaste";
import { genPwd } from "@/core/lib/etc";

type PropsType = {
  swapMode?: SwapModeT;
  isCurrSwap?: boolean;
};

const PwdGenerator: FC<PropsType> = ({
  swapMode = "swapped",
  isCurrSwap = true,
}) => {
  const [pwd, setPwd] = useState("");

  genPwd();

  return (
    <div className="w-full flex items-center gap-10">
      <div className="w-fit">
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

      <div className="w-fit">
        <CpyPaste {...{ txt: pwd }} />
      </div>
    </div>
  );
};

export default PwdGenerator;
