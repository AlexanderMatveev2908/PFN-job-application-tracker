/** @jsxImportSource @emotion/react */
"use client";

import SearchBar from "@/features/layout/components/SearchBar/SearchBar";
import { filtersSearchJobs, searchJobsFieldsTxt } from "./uiFactory";
import { resetValsSearchJobs, SearchJobsFormT } from "./paperwork";
import { FormFieldTxtSearchBarT } from "@/common/types/ui";
import { FC } from "react";

const SearchJobs: FC = () => {
  return (
    <SearchBar
      {...{
        allowedTxtFields:
          searchJobsFieldsTxt as FormFieldTxtSearchBarT<SearchJobsFormT>[],
        resetVals: resetValsSearchJobs,
        filters: filtersSearchJobs,
      }}
    />
  );
};

export default SearchJobs;
