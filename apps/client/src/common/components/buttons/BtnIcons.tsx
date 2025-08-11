/** @jsxImportSource @emotion/react */
"use client";

import { FC } from "react";
import { FaCloud, FaDatabase, FaGear, FaServer } from "react-icons/fa6";
import { IoGitNetwork } from "react-icons/io5";
import { LiaCookieSolid } from "react-icons/lia";
type PropsType = {
  label: string;
  type?: "button" | "submit";
  handleClick?: () => void;
  isEnabled?: boolean;
  isLoading?: boolean;
};

const BtnIcons: FC<PropsType> = ({
  isEnabled,
  label,
  type = "button",
  handleClick,
}) => {
  return (
    <button
      onClick={handleClick}
      type={type}
      disabled={isEnabled!}
      className="btn_icons w-full transition-all duration-500 relative enabled:cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <div className="relative w-full overflow-hidden rounded-xl">
        <div className="btn_icons__content">
          <span className={`relative z-40 txt__lg`}>{label}</span>
        </div>

        <span className="btn_icons__ref_0"></span>
        <span className="btn_icons__ref_1"></span>
      </div>

      <span className="btn_icons__shadow"></span>

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
