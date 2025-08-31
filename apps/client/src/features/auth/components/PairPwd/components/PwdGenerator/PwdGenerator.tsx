/** @jsxImportSource @emotion/react */
"use client";

import SvgPasswordCursor from "@/common/components/SVGs/PasswordCursor";
import { useState, type FC } from "react";
import BtnSvg from "@/common/components/buttons/BtnSvg";
import { SwapModeT } from "@/app/auth/register/page";
import CpyPaste from "@/common/components/elements/tooltips/CpyPaste/CpyPaste";
import { genPwd } from "@/core/lib/etc";
import { isStr } from "@/core/lib/dataStructure";
import { css } from "@emotion/react";
import { resp } from "@/core/lib/style";

type PropsType = {
  swapMode?: SwapModeT;
  isCurrSwap?: boolean;
};

const PwdGenerator: FC<PropsType> = ({
  swapMode = "swapped",
  isCurrSwap = true,
}) => {
  const [pwd, setPwd] = useState("");

  return (
    <div
      className="w-full grid"
      css={css`
        grid-template-columns: 1fr;
        gap: 1.5rem;

        ${resp(450)} {
          grid-template-columns: 75px 1fr;
        }
      `}
    >
      <div className="w-fit">
        <BtnSvg
          {...{
            testID: "pwd_generator__btn",
            Svg: SvgPasswordCursor,
            handleClick: () => setPwd(genPwd),
            confPortal: {
              optDep: [swapMode],
              showPortal: swapMode === "swapped" && isCurrSwap,
              txt: "Generate Password",
            },
          }}
        />
      </div>

      {isStr(pwd) && (
        <div className="w-fit">
          <CpyPaste
            {...{
              testID: "pwd_generator__result",
              txt: pwd,
              portalConf: {
                optDep: [swapMode],
                showPortal: swapMode === "swapped" && isCurrSwap,
              },
            }}
          />
        </div>
      )}
    </div>
  );
};

export default PwdGenerator;
