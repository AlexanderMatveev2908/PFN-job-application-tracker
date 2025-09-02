/** @jsxImportSource @emotion/react */
"use client";

import { usePathname } from "next/navigation";
import type { FC } from "react";
import { spannerLinks, SpannerLinksAuthT } from "./uiFactory/idx";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import { LinkAppSvgT } from "@/common/types/ui";
import LinkSvg from "@/common/components/links/LinkSvg";
import { extractNamePagePath } from "@/core/lib/path";

const SpannerLinks: FC = () => {
  const p = usePathname();
  const isAuthLayout = p.includes("/auth");

  const links =
    spannerLinks[
      extractNamePagePath(p, { usFriendly: false }) as SpannerLinksAuthT
    ];
  const { ids } = useGenIDs({ lengths: [links.length] });

  return !isAuthLayout ? null : (
    <div className="w-full grid grid-cols-2 items-center justify-items-center py-[25px]">
      {links.map((el, i) => {
        const Svg = (el.link as LinkAppSvgT).Svg;

        return (
          <LinkSvg
            key={ids[0][i]}
            {...{
              href: (el.link as LinkAppSvgT).href,
              Svg,
              confPortal: {
                showPortal: true,
                txt: el.msg as string,
              },
            }}
          />
        );
      })}
    </div>
  );
};

export default SpannerLinks;
