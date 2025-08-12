/** @jsxImportSource @emotion/react */
"use client";

import { AppEventT } from "@/common/types/api";
import { PortalConfT } from "@/common/types/ui";
import { CSSProperties, useMemo, useState, type FC } from "react";
import { IconType } from "react-icons";
import { $argClr } from "@/core/uiFactory/style";
import { useSyncPortal } from "@/core/hooks/ui/useSyncPortal";
import { css } from "@emotion/react";
import { isObjOk } from "@/core/lib/dataStructure";
import PortalWrapper from "./PortalWrapper";
import Link from "next/link";
import { RefObject } from "react";

type PropsType = {
  wrapper: "html_button" | "next_link";
  Svg: IconType;
  propsLink?: {
    href: string;
  };
  propsBtn?: {
    isEnabled?: boolean;
    handleClick: () => void;
  };
  act?: AppEventT;
  confPortal?: PortalConfT & { txt: string };
};

const SvgTooltip: FC<PropsType> = ({
  Svg,
  act = "NONE",
  confPortal,
  wrapper,
  propsLink,
  propsBtn,
}) => {
  const [isHover, setIsHover] = useState(false);
  const $clr = $argClr[act];

  const { coords, parentRef } = useSyncPortal(confPortal?.optDep);

  const objProps = useMemo(
    () => ({
      onMouseEnter: () => setIsHover(true),
      onMouseLeave: () => setIsHover(false),
      ref: parentRef,
      className: `${
        wrapper === "html_button" ? "btn__app" : "el__app"
      } flex items-center justify-center relative`,
      css: css`
        color: ${$clr};
      `,
      style: {
        "--scale__up": 1.3,
      } as CSSProperties,
    }),
    [$clr, parentRef, wrapper]
  );

  const content = (
    <>
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
    </>
  );

  return wrapper === "html_button" ? (
    <button
      disabled={propsBtn!.isEnabled!}
      onClick={propsBtn!.handleClick}
      {...(objProps as typeof objProps & { ref: RefObject<HTMLButtonElement> })}
    >
      {content}
    </button>
  ) : (
    <Link
      href={propsLink!.href}
      {...(objProps as typeof objProps & { ref: RefObject<HTMLAnchorElement> })}
    >
      {content}
    </Link>
  );
};

export default SvgTooltip;
