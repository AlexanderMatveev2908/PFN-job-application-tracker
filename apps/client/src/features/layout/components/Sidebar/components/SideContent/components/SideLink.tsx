/** @jsxImportSource @emotion/react */
"use client";

import { LinkAppSvgT } from "@/common/types/ui";
import Link from "next/link";
import type { FC } from "react";

type PropsType = {
  lk: LinkAppSvgT;
  isCurrPath: boolean;
  handleClick: () => void;
};

const SideLink: FC<PropsType> = ({ lk, isCurrPath, handleClick }) => {
  return (
    <Link
      href={lk.href}
      onClick={handleClick}
      className={`link__app ${
        isCurrPath && "link__curr"
      } flex items-center justify-start gap-6`}
    >
      <lk.Svg className="svg__lg" fill={lk.fill} />

      <span className="txt__lg">{lk.label}</span>
    </Link>
  );
};

export default SideLink;
