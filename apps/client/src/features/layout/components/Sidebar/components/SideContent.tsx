/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { sideLinksAll } from "../uiFactory/idx";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import SideLink from "./components/SideLink";
import { usePathname } from "next/navigation";
import { calcIsCurrPath } from "@/core/lib/etc";

const SideContent: FC = () => {
  const { ids } = useGenIDs({
    lengths: [sideLinksAll.length],
  });

  const path = usePathname();

  return (
    <div className="w-full flex flex-col gap-8 items-start">
      {sideLinksAll.map((lk, i) => (
        <SideLink
          key={ids[0][i]}
          {...{ lk, isCurrPath: calcIsCurrPath(path, lk.href) }}
        />
      ))}
    </div>
  );
};

export default SideContent;
