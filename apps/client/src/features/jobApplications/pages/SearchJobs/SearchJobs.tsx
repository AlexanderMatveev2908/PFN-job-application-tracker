/** @jsxImportSource @emotion/react */
"use client";

import SearchBar from "@/features/layout/components/SearchBar/SearchBar";
import { searchJobsFieldsTxt } from "../../uiFactory/searchJobs";
import {
  resetValsSearchJobs,
  SearchJobsFormT,
} from "../../paperwork/searchJobs";
import { FormFieldTxtSearchBarT } from "@/common/types/ui";
import { FC } from "react";
import { useSearchCtxConsumer } from "@/features/layout/components/SearchBar/context/hooks/ctxConsumer";

const SearchJobs: FC = () => {
  const ctx = useSearchCtxConsumer();

  console.log(ctx);

  return (
    <SearchBar
      {...{
        allowedTxtFields:
          searchJobsFieldsTxt as FormFieldTxtSearchBarT<SearchJobsFormT>[],
        resetVals: resetValsSearchJobs,
      }}
    />
  );
};

export default SearchJobs;
