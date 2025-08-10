/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import {
  sideDropAccount,
  sideLinkLogout,
  sideLinksAll,
  sideLinksLogged,
  sideLinksNonLogged,
} from "./uiFactory/idx";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import SideLink from "./components/SideLink";
import { usePathname } from "next/navigation";
import { calcIsCurrPath } from "@/core/lib/etc";
import DropMenuStatic from "@/common/components/dropMenus/DropMenuStatic";
import { useDispatch } from "react-redux";
import { sideSlice } from "../../slice";

const SideContent: FC = () => {
  const { ids } = useGenIDs({
    lengths: [
      sideLinksAll.length,
      sideLinksLogged.length,
      sideLinksNonLogged.length,
    ],
  });

  const dispatch = useDispatch();
  const path = usePathname();

  const handleClick = () => dispatch(sideSlice.actions.closeSide());

  return (
    <div className="w-full flex flex-col gap-8 items-start">
      {sideLinksAll.map((lk, i) => (
        <SideLink
          key={ids[0][i]}
          {...{ lk, isCurrPath: calcIsCurrPath(path, lk.href), handleClick }}
        />
      ))}
      {sideLinksLogged.map((lk, i) => (
        <SideLink
          key={ids[1][i]}
          {...{ lk, isCurrPath: calcIsCurrPath(path, lk.href), handleClick }}
        />
      ))}

      <DropMenuStatic {...{ el: sideDropAccount }}>
        {sideLinksNonLogged.map((lk, i) => (
          <SideLink
            key={ids[2][i]}
            {...{ lk, isCurrPath: calcIsCurrPath(path, lk.href), handleClick }}
          />
        ))}
      </DropMenuStatic>

      <SideLink {...{ lk: sideLinkLogout, isCurrPath: false, handleClick }} />
    </div>
  );
};

export default SideContent;
