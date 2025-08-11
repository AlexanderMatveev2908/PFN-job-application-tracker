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
      className="btn_container"
    >
      <div className="btn_container__content">
        <div className="content__btn">
          <span className={`relative z-40 txt__lg`}>{label}</span>
        </div>

        <span className="btn__ref_1"></span>
        <span className="btn__ref_2"></span>
      </div>

      <span className="btn_container__shadow"></span>

      <FaDatabase className="btn_container__svg_1" />
      <FaGear className="btn_container__svg_2" />
      <FaCloud className="btn_container__svg_3" />
      <FaServer className="btn_container__svg_4" />
      <IoGitNetwork className="btn_container__svg_5" />
      <LiaCookieSolid className="btn_container__svg_6" />
    </button>
  );
};
export default BtnIcons;
