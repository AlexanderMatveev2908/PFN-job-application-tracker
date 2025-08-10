/** @jsxImportSource @emotion/react */
"use client";

import { useRef, useState, type FC } from "react";
import { css, SerializedStyles } from "@emotion/react";
import { ChildrenT, FieldTxtSvgT } from "@/common/types/ui";
import PairTxtSvg from "../elements/PairTxtSvg";
import { useMouseOut } from "@/core/hooks/ui/useMouseOut";

type PropsType = {
  el: FieldTxtSvgT;
  $SvgCls?: string;
  $customCSS?: SerializedStyles;
} & ChildrenT;

const DropMenuAbsolute: FC<PropsType> = ({
  el,
  $SvgCls,
  children,
  $customCSS,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropRef = useRef(null);

  useMouseOut({
    ref: dropRef,
    cb: () => setIsOpen(false),
  });

  return (
    <div ref={dropRef} className="w-full relative">
      <button
        onClick={() => setIsOpen((prev) => !prev)}
        className={`btn__app w-full cursor-pointer p-[6px] bd__sm ${
          isOpen
            ? "text-neutral-950 bg-neutral-200"
            : "text-neutral-300 hover:text-neutral-950"
        } hover:bg-neutral-300`}
        style={
          {
            "--scale__up": 1.2,
          } as React.CSSProperties
        }
      >
        <PairTxtSvg {...{ el, $SvgCls }} />
      </button>

      <div
        className="absolute w-full min-w-[300px] max-w-[350px] h-fit overflow-y-auto scroll__app bg-neutral-950 z-60 bd__md rounded-xl"
        css={css`
          ${$customCSS}
          top: calc(100% + 10px);
          transition: transform 0.4s, opacity 0.3s;
          transform: translateY(${isOpen ? "0" : "75px"});
          opacity: ${isOpen ? 1 : 0};
        `}
      >
        <div
          onClick={() => setIsOpen(false)}
          className="w-full flex flex-col max-h-[200px] scroll__app overflow-y-auto"
        >
          {children}
        </div>
      </div>
    </div>
  );
};

export default DropMenuAbsolute;
