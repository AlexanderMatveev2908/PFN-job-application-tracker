/** @jsxImportSource @emotion/react */
"use client";

import { AppEventT } from "@/common/types/api";
import { css } from "@emotion/react";
import { FC } from "react";
import { FaCloud, FaDatabase, FaGear, FaServer } from "react-icons/fa6";
import { IoGitNetwork } from "react-icons/io5";
import { LiaCookieSolid } from "react-icons/lia";
import { $argClr } from "@/core/uiFactory/style";
type PropsType = {
  label: string;
  type?: "button" | "submit";
  handleClick?: () => void;
  isEnabled?: boolean;
  isLoading?: boolean;
  act?: AppEventT;
};

const BtnIcons: FC<PropsType> = ({
  isEnabled,
  label,
  type = "button",
  handleClick,
  act = "NONE",
}) => {
  const $clr = $argClr[act];

  return (
    <button
      onClick={handleClick}
      type={type}
      disabled={isEnabled!}
      className="btn_icons btn__app w-full transition-all duration-500 relative"
      css={css`
        .btn_icons__content,
        .btn_icons__shadow {
          padding: 0.5rem 1rem;
          transition: 0.3s;
          border-radius: 1rem;
          background: var(--neutral__950);
          /* overflow: hidden; */

          &::after {
            content: "";
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            border-radius: 1rem;
            background: transparent;
            border: 3px solid ${$clr};
            z-index: 10;
          }
        }

        &:enabled:hover {
          rotate: -5deg;
          transform: scale(1.1);

          .btn_icons__shadow {
            transform: translate(-4%, 15%);
          }
        }
      `}
    >
      <div
        className="relative w-full rounded-xl"
        css={css`
          /* overflow: hidden; */
        `}
      >
        <div className="btn_icons__content relative">
          <span className={`relative z-40 txt__lg`}>{label}</span>
        </div>

        <span className="btn_icons__ref_0"></span>
        <span className="btn_icons__ref_1"></span>
      </div>

      <span className="btn_icons__shadow absolute inset-0 -z-10"></span>

      <FaDatabase className="btn_icons__svg_0" />
      <FaGear className="btn_icons__svg_1" />
      <FaCloud className="btn_icons__svg_2" />
      <FaServer className="btn_icons__svg_3" />
      <IoGitNetwork className="btn_icons__svg_4" />
      <LiaCookieSolid className="btn_icons__svg_5" />
    </button>
  );
};
export default BtnIcons;
