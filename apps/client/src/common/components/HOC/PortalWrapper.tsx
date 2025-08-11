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
} & ChildrenT;

const PortalWrapper: FC<PropsType> = ({ $CSS, children, act = "NONE" }) => {
  const $clr = $argClr[act];

  return (
    <Portal>
      <div
        className="absolute w-fit h-fit bg-neutral-950 border-2 rounded-xl"
        css={css`
          z-index: 100;
          border-color: ${$clr};
          ${$CSS}
        `}
      >
        {children}

        <TriangleTooltip
          {...{
            $clr,
            $sizeTrg: 50,
          }}
        />
      </div>
    </Portal>
  );
};

export default PortalWrapper;
