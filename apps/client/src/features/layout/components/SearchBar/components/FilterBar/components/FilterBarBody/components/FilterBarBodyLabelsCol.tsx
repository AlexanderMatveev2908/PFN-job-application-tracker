/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { genLorem } from "@/core/lib/etc";
import FilterBarBodyWrapCol from "./subComponents/FilterBarBodyWrapCol";

type PropsType = {};

const FilterBarBodyLabelsCol: FC<PropsType> = ({}) => {
  return <FilterBarBodyWrapCol>{genLorem(20)}</FilterBarBodyWrapCol>;
};

export default FilterBarBodyLabelsCol;
