/** @jsxImportSource @emotion/react */
"use client";

import SvgBurger from "@/common/components/SVGs/Burger";
import SvgLogo from "@/common/components/SVGs/Logo";
import SvgUser from "@/common/components/SVGs/User";
import { css } from "@emotion/react";
import Link from "next/link";
import type { FC } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getSideState, sideSlice } from "../Sidebar/slice";
import SvgClose from "@/common/components/SVGs/Close";

const Header: FC = () => {
  const sideState = useSelector(getSideState);

  const dispatch = useDispatch();
  return (
    <div
      className="z__header w-full sticky top-0 left-0 border-b-3 border-w_0 flex items-center justify-between px-3"
      css={css`
        height: ${75}px;
      `}
    >
      <Link href={"/"}>
        <SvgLogo className="svg__xl" />
      </Link>

      <div className="w-fit flex items-center gap-14">
        <button>
          <SvgUser className="svg__xl text-w_0" />
        </button>

        <button
          onClick={() => dispatch(sideSlice.actions.toggleSide())}
          className="btn__app"
          style={
            {
              "--scale__up": 1.3,
            } as React.CSSProperties
          }
        >
          {sideState.isOpen ? (
            <SvgClose className="svg__xl text-red-600" />
          ) : (
            <SvgBurger className="svg__xl text-w_0" />
          )}
        </button>
      </div>
    </div>
  );
};

export default Header;
