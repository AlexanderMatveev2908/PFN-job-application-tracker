/** @jsxImportSource @emotion/react */
"use client";

import { LinkAppSvgT } from "@/common/types/ui";
import Link from "next/link";
import type { FC } from "react";

type PropsType = {
  lk: LinkAppSvgT;
};

const SideLink: FC<PropsType> = ({ lk }) => {
  return (
    <Link href={lk.href} className="flex items-center justify-start gap-6">
      <lk.Svg className="svg__lg" />

      <span className="txt__lg">{lk.label}</span>
    </Link>
  );
};

export default SideLink;
