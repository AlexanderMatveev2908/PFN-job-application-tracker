/** @jsxImportSource @emotion/react */
"use client";

import SvgBurger from "@/common/components/SVGs/Burger";
import SvgLogo from "@/common/components/SVGs/Logo";
import SvgUser from "@/common/components/SVGs/User";
import { css } from "@emotion/react";
import Link from "next/link";
import type { FC } from "react";

const Header: FC = () => {
  return (
    <div
      className="w-full sticky top-0 left-0 border-b-3 border-w_0 flex items-center justify-between px-3"
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

        <button>
          <SvgBurger className="svg__xl text-w_0" />
        </button>
      </div>
    </div>
  );
};

export default Header;
