/** @jsxImportSource @emotion/react */
"use client";

import { DropElT } from "@/common/types/ui";
import { ReactNode, useState, type FC } from "react";
import { css } from "@emotion/react";
import { FaChevronDown } from "react-icons/fa6";

type PropsType = {
  el: DropElT;
  children: ReactNode;
};

const DropMenuStatic: FC<PropsType> = ({ el, children }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="w-full flex flex-col">
      <div
        onClick={() => setIsOpen((prev) => !prev)}
        className={`${
          isOpen
            ? "text-neutral-950 bg-neutral-200"
            : "text-neutral-300 hover:text-neutral-950 "
        } w-full flex items-center justify-between transition-all duration-300 hover:bg-neutral-300 cursor-pointer rounded-xl px-4 py-2`}
      >
        <div className="flex items-center justify-start gap-6">
          {el.Svg && <el.Svg className="svg__md" />}

          <span className="txt__lg">{el.label}</span>
        </div>

        <FaChevronDown
          className="svg__sm"
          css={css`
            transition: 0.3s transform;
            transform: rotate(${isOpen ? 180 : 0}deg);
          `}
        />
      </div>

      <div
        className="scroll__app overflow-y-auto flex w-full flex-col gap-4 py-3"
        css={css`
          transition: opacity 0.3s, max-height 0.4s;
          max-height: ${isOpen ? 10 ** 3 : 0}px;
          opacity: ${isOpen ? 1 : 0};
        `}
      >
        {children}
      </div>
    </div>
  );
};

export default DropMenuStatic;
