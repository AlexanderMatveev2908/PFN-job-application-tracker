/** @jsxImportSource @emotion/react */
"use client";

import SvgBurger from "@/common/components/SVGs/Burger";
import SvgLogo from "@/common/components/SVGs/Logo";
import { css } from "@emotion/react";
import Link from "next/link";
import { useRef, type FC } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getSideState, sideSlice } from "../Sidebar/slice";
import SvgClose from "@/common/components/SVGs/Close";
import { TbUserFilled } from "react-icons/tb";
import DropMenuAbsolute from "@/common/components/dropMenus/DropMenuAbsolute";
import { linksAll, linksNonLogged } from "@/core/uiFactory/links";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import HeaderLink from "./components/HeaderLink";
import { calcIsCurrPath } from "@/core/lib/etc";
import { usePathname } from "next/navigation";
import { headerHight } from "@/core/constants/style";
import { useHydration } from "@/core/hooks/ui/useHydration";
import { useGetUserState } from "@/features/user/hooks/useGetUserState";
import { extractInitialsUser } from "@/core/lib/formatters";

const Header: FC = () => {
  const sideState = useSelector(getSideState);
  const usState = useGetUserState();
  const dropRef = useRef(null);

  const { isHydrated } = useHydration();

  const path = usePathname();
  const dispatch = useDispatch();

  const { ids } = useGenIDs({
    lengths: [linksAll.length + linksNonLogged.length],
  });

  return (
    <div
      className="z__header w-full sticky top-0 left-0 border-b-3 bg-neutral-950 border-w__0 flex items-center justify-between px-3"
      css={css`
        height: ${headerHight}px;
      `}
    >
      <Link href={"/"}>
        <SvgLogo className="svg__xl" />
      </Link>

      <div ref={dropRef} className="w-fit flex items-center gap-14">
        <DropMenuAbsolute
          {...{
            isEnabled: isHydrated,
            testID: "header__toggle_drop",
            el: {
              Svg: !usState.isUsOk ? TbUserFilled : null,
              label: usState.isUsOk
                ? extractInitialsUser(usState!.user!)
                : null,
            },
            $SvgCls: "svg__sm",
            $customCSS: css`
              left: -200px;
            `,
          }}
        >
          {[...linksAll, ...(!usState.isUsOk ? linksNonLogged : [])].map(
            (lk, i) => (
              <HeaderLink
                key={ids[0][i]}
                {...{
                  isCurrPath: calcIsCurrPath(path, lk.href),
                  lk,
                  handleClick: () => null,
                }}
              />
            )
          )}
        </DropMenuAbsolute>

        <button
          disabled={!isHydrated}
          data-testid={"header__toggle_sidebar"}
          key={sideState.isOpen + ""}
          onClick={() => dispatch(sideSlice.actions.toggleSide())}
          className="btn__app"
          style={
            {
              "--scale__up": 1.3,
            } as React.CSSProperties
          }
        >
          {sideState.isOpen ? (
            <SvgClose className="svg__xl" fill="var(--red__600)" />
          ) : (
            <SvgBurger className="svg__xl text-w__0" />
          )}
        </button>
      </div>
    </div>
  );
};

export default Header;
