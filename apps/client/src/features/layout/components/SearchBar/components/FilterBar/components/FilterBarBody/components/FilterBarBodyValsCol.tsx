/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { genLorem } from "@/core/lib/etc";
import FilterBarBodyWrapCol from "./subComponents/FilterBarBodyWrapCol";
import { FilterSearchBarT } from "@/features/layout/components/SearchBar/types";

type PropsType = {
  filters: FilterSearchBarT[];
};

const FilterBarBodyValsCol: FC<PropsType> = ({}) => {
  return <FilterBarBodyWrapCol>{genLorem(20)}</FilterBarBodyWrapCol>;
};

export default FilterBarBodyValsCol;
