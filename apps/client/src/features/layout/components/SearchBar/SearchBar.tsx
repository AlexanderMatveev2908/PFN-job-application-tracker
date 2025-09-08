/** @jsxImportSource @emotion/react */
"use client";

import Shim from "@/common/components/elements/Shim";
import { useHydration } from "@/core/hooks/etc/hydration/useHydration";
import { css } from "@emotion/react";
import type { FC } from "react";

type PropsType = {};

const SearchBar: FC<PropsType> = ({}) => {
  const { isHydrated } = useHydration();

  return !isHydrated ? (
    <Shim
      {...{
        $CSS: css`
          width: 95%;
          max-width: 1200px;
          height: 200px;
        `,
      }}
    />
  ) : (
    <div className="w-full max-w-[1200px] h-fit min-h-[200px] border-3 border-w__0 rounded-xl p-5"></div>
  );
};

export default SearchBar;
