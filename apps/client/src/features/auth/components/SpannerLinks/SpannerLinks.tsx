/** @jsxImportSource @emotion/react */
"use client";

import { usePathname } from "next/navigation";
import type { FC } from "react";
import { spannerLinks, SpannerLinksAuthT } from "./uiFactory/idx";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import { LinkAppSvgT } from "@/common/types/ui";

const SpannerLinks: FC = () => {
  const p = usePathname();
  const last = p.split("/").pop();

  const links = spannerLinks[last as SpannerLinksAuthT];
  const { ids } = useGenIDs({ lengths: [links.length] });

  return (
    <div className="w-full grid grid-cols-2 items-center justify-items-center py-[25px]">
      {links.map((el, i) => {
        const Svg = (el.link as LinkAppSvgT).Svg;

        return (
          <div key={ids[0][i]} className="flex">
            <Svg className="svg__md" />
            <span></span>
          </div>
        );
      })}
    </div>
  );
};

export default SpannerLinks;
