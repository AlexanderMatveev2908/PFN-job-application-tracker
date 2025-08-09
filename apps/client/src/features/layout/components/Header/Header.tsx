/** @jsxImportSource @emotion/react */
"use client";

import SvgBurger from "@/common/components/SVGs/Burger";
import SvgLogo from "@/common/components/SVGs/Logo";
import { css } from "@emotion/react";
import Link from "next/link";
import type { FC } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getSideState, sideSlice } from "../Sidebar/slice";
import SvgClose from "@/common/components/SVGs/Close";
import { TbUserFilled } from "react-icons/tb";

const Header: FC = () => {
  const sideState = useSelector(getSideState);

  const dispatch = useDispatch();
  return (
    <div
      className="z__header w-full sticky top-0 left-0 border-b-3 border-w__0 flex items-center justify-between px-3"
      css={css`
        height: ${75}px;
      `}
    >
      <Link href={"/"}>
        <SvgLogo className="svg__xl" />
      </Link>

      <div className="w-fit flex items-center gap-14">
        <button>
          <TbUserFilled className="svg__md text-w__0" fill="var(--white__0)" />
        </button>

        <button
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
