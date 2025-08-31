/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { sideDropAccount, sideLinksLogged } from "./uiFactory/idx";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import SideLink from "./components/SideLink";
import { usePathname } from "next/navigation";
import { calcIsCurrPath } from "@/core/lib/etc";
import DropMenuStatic from "@/common/components/dropMenus/DropMenuStatic";
import { useDispatch } from "react-redux";
import { sideSlice } from "../../slice";
import { linkLogout, linksAll, linksNonLogged } from "@/core/uiFactory/links";
import { useGetUserState } from "@/features/user/hooks/useGetUserState";

const SideContent: FC = () => {
  const { ids } = useGenIDs({
    lengths: [linksAll.length, sideLinksLogged.length, linksNonLogged.length],
  });

  const isUsOk = useGetUserState().isUsOk;
  const dispatch = useDispatch();
  const path = usePathname();

  const handleClick = () => dispatch(sideSlice.actions.closeSide());

  return (
    <div className="w-full flex flex-col gap-8 items-start">
      {linksAll.map((lk, i) => (
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

      {!isUsOk && (
        <DropMenuStatic {...{ el: sideDropAccount }}>
          {linksNonLogged.map((lk, i) => (
            <SideLink
              key={ids[2][i]}
              {...{
                lk,
                isCurrPath: calcIsCurrPath(path, lk.href),
                handleClick,
              }}
            />
          ))}
        </DropMenuStatic>
      )}

      {isUsOk && (
        <SideLink {...{ lk: linkLogout, isCurrPath: false, handleClick }} />
      )}
    </div>
  );
};

export default SideContent;
