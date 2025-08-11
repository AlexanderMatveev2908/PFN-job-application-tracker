/** @jsxImportSource @emotion/react */
"use client";

import PortalWrapper from "@/common/components/HOC/PortalWrapper";

import { css } from "@emotion/react";
import type { FC } from "react";

type PropsType = {
  coords: number[];
};

const PwdMatchTracker: FC<PropsType> = ({ coords }) => {
  return (
    <PortalWrapper
      {...{
        $CSS: css`
          top: ${coords[0]}px;
          left: ${coords[1]}px;
        `,
        act: "INFO",
      }}
    >
      <div className="w-[75vw] h-[200px] p-5"></div>
    </PortalWrapper>
  );
};

export default PwdMatchTracker;
