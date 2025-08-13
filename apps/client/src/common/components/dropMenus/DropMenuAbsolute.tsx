/** @jsxImportSource @emotion/react */
"use client";

import { useRef, useState, type FC } from "react";
import { css, SerializedStyles } from "@emotion/react";
import { ChildrenT, FieldTxtSvgT, TestIdT } from "@/common/types/ui";
import PairTxtSvg from "../elements/PairTxtSvg";
import { useMouseOut } from "@/core/hooks/ui/useMouseOut";

type PropsType = {
  el: FieldTxtSvgT;
  isEnabled?: boolean;
  $SvgCls?: string;
  $customCSS?: SerializedStyles;
} & ChildrenT &
  TestIdT;

const DropMenuAbsolute: FC<PropsType> = ({
  el,
  $SvgCls,
  isEnabled = true,
  children,
  $customCSS,
  t_id,
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
        disabled={!isEnabled}
        data-testid={t_id}
        onClick={() => setIsOpen((prev) => !prev)}
        className={`btn__app w-full cursor-pointer p-[6px] border-2 bd__sm ${
          isOpen
            ? "text-neutral-950 bg-neutral-200"
            : "text-neutral-300 enabled:hover:text-neutral-950"
        } enabled:hover:bg-neutral-300`}
        style={
          {
            "--scale__up": 1.2,
          } as React.CSSProperties
        }
      >
        <PairTxtSvg {...{ el, $SvgCls }} />
      </button>

      <div
        data-testid={"drop_menu_absolute__content"}
        className="absolute w-full min-w-[300px] max-w-[350px] h-fit overflow-y-auto scroll__app bg-neutral-950 z-60 border-3 border-neutral-200 rounded-xl"
        css={css`
          ${$customCSS}
          top: calc(100% + 10px);
          transition: transform 0.4s, opacity 0.3s;
          transform: translateY(${isOpen ? "0" : "75px"});
          opacity: ${isOpen ? 1 : 0};
          pointer-events: ${isOpen ? "auto" : "none"};
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
