/** @jsxImportSource @emotion/react */
"use client";

import { css } from "@emotion/react";
import type { FC } from "react";
import { SorterSearchBarT } from "../../../types";

type PropsType = {
  sorters: SorterSearchBarT[];
};

const SortBarBody: FC<PropsType> = ({}) => {
  return (
    <div
      className="flex flex-col overflow-y-auto scroll__app min-h-0"
      css={css`
        max-height: calc(100% - 100px);
      `}
    ></div>
  );
};

export default SortBarBody;
