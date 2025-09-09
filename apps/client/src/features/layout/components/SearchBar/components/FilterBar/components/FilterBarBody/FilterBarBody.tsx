/** @jsxImportSource @emotion/react */
"use client";

import { css } from "@emotion/react";
import type { FC } from "react";
import FilterBarBodyLabelsCol from "./components/FilterBarBodyLabelsCol";
import FilterBarBodyValsCol from "./components/FilterBarBodyValsCol";

type PropsType = {};

const FilterBarBody: FC<PropsType> = ({}) => {
  return (
    <div
      className="w-full grid grid-cols-[80px_3px_1fr] md:grid-cols-[250px_3px_1fr] relative"
      css={css`
        height: 100%;
      `}
    >
      <FilterBarBodyLabelsCol />
      <div className="w-full min-h-full bg-neutral-800"></div>
      <FilterBarBodyValsCol />
    </div>
  );
};

export default FilterBarBody;
