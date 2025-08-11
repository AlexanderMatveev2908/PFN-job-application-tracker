/** @jsxImportSource @emotion/react */
"use client";

import PortalWrapper from "@/common/components/HOC/PortalWrapper";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";

import { css } from "@emotion/react";
import type { FC } from "react";
import { rulesPwd } from "./uiFactory/idx";

type PropsType = {
  coords: number[];
};

const PwdMatchTracker: FC<PropsType> = ({ coords }) => {
  const { ids } = useGenIDs({ lengths: [rulesPwd.length] });

  return (
    <PortalWrapper
      {...{
        $CSS: css`
          top: ${coords[0]}px;
          left: ${coords[1]}px;
        `,
        act: "INFO",
        $trgCtmCSS: css`
          left: 15%;
        `,
      }}
    >
      <div className="w-[75vw] max-w-[600px] h-[200px] p-5"></div>
    </PortalWrapper>
  );
};

export default PwdMatchTracker;
