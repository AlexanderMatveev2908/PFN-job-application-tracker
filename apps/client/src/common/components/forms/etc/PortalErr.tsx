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
      <ErrField
        {...{
          msg,
          $ctmCSS: css`
            top: ${coords.top}px;
            right: ${coords.right}px;
          `,
        }}
      />
    </Portal>
  );
};

export default PortalErr;
