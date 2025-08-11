/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import Portal from "../elements/Portal";
import { css } from "@emotion/react";
import { SerializedStyles } from "@emotion/react";
import { ChildrenT } from "@/common/types/ui";
import { AppEventT } from "@/common/types/api";
import { $argClr } from "@/core/uiFactory/style";
import TriangleTooltip from "../elements/Tooltip/subComponents/TriangleTooltip";

type PropsType = {
  $CSS: SerializedStyles;
  act?: AppEventT;
  $trgCtmCSS?: SerializedStyles;
  isHover: boolean;
} & ChildrenT;

const PortalWrapper: FC<PropsType> = ({
  $CSS,
  $trgCtmCSS,
  children,
  act = "NONE",
  isHover,
}) => {
  const $clr = $argClr[act];

  return (
    <Portal>
      <div
        className="absolute w-fit h-fit bg-neutral-950 border-2 rounded-xl pointer-events-none z-60"
        css={css`
          border-color: ${$clr};
          ${$CSS}
          transition: transform 0.4s, opacity 0.3s;
          transform: translateY(${isHover ? "-100" : ""}%);
          opacity: ${isHover ? 1 : 0};
        `}
      >
        {children}

        <TriangleTooltip
          {...{
            $clr,
            $sizeTrg: 50,
            $trgCtmCSS,
          }}
        />
      </div>
    </Portal>
  );
};

export default PortalWrapper;
