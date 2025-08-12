/** @jsxImportSource @emotion/react */
"use client";

import { AppEventT } from "@/common/types/api";
import { css } from "@emotion/react";
import { RefObject, useState, type FC } from "react";
import { $argClr } from "@/core/uiFactory/style";
import { IconType } from "react-icons";
import PortalWrapper from "../HOC/shapes/PortalWrapper";
import { useSyncPortal } from "@/core/hooks/ui/useSyncPortal";
import { PortalConfT } from "@/common/types/ui";
import { isObjOk } from "@/core/lib/dataStructure";

type PropsType = {
  handleClick: () => void;
  Svg: IconType;
  act?: AppEventT;
  isEnabled?: boolean;
  confPortal?: PortalConfT & { txt: string };
};

const BtnSvg: FC<PropsType> = ({
  handleClick,
  act = "NONE",
  Svg,
  isEnabled = true,
  confPortal,
}) => {
  const [isHover, setIsHover] = useState(false);
  const $clr = $argClr[act];

  const { coords, parentRef } = useSyncPortal(confPortal?.optDep);

  return (
    <button
      onMouseEnter={() => setIsHover(true)}
      onMouseLeave={() => setIsHover(false)}
      type="button"
      ref={parentRef as RefObject<HTMLButtonElement>}
      onClick={handleClick}
      disabled={!isEnabled}
      className="btn__app flex items-center justify-center relative"
      css={css`
        color: ${$clr};
      `}
      style={
        {
          "--scale__up": 1.3,
        } as React.CSSProperties
      }
    >
      {isObjOk(confPortal) && (
        <PortalWrapper
          {...{
            isHover: isHover && confPortal!.showPortal,
            act: "NONE",
            $CSS: css`
              top: ${coords.top - 25}px;
              left: ${coords.left - 25}px;
            `,
            $trgCtmCSS: css`
              left: 15%;
            `,
            $sizeTrg: 30,
          }}
        >
          <span className="txt__md py-2 px-4 inline-block min-w-[200px] max-w-[400px] break-all">
            {confPortal!.txt}
          </span>
        </PortalWrapper>
      )}

      <Svg className="svg__lg" />
    </button>
  );
};

export default BtnSvg;
