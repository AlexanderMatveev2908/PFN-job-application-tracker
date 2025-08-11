/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import Portal from "../../elements/Portal";
import ErrField from "./ErrField";
import { css } from "@emotion/react";
import { CoordsTooltipT } from "@/core/hooks/ui/useSyncPortal";

type PropsType = {
  coords: CoordsTooltipT;
  msg?: string;
  showPortal: boolean;
};

const PortalErr: FC<PropsType> = ({ msg, coords, showPortal }) => {
  return !showPortal ? null : (
    <Portal>
      <div
        className="w-full h-full absolute z-60 pointer-events-none"
        css={css`
          top: ${coords.top}px;
          right: ${coords.right}px;
        `}
      >
        <ErrField {...{ msg }} />
      </div>
    </Portal>
  );
};

export default PortalErr;
