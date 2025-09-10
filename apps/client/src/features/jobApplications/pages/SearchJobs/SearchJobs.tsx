/** @jsxImportSource @emotion/react */
"use client";

import SearchBar from "@/features/layout/components/SearchBar/SearchBar";
import {
  filtersSearchJobs,
  searchJobsFieldsTxt,
  sortersSearchJobs,
} from "./uiFactory";
import { resetValsSearchJobs, SearchJobsFormT } from "./paperwork";
import { FormFieldTxtSearchBarT } from "@/common/types/ui";
import { FC } from "react";
import { useSelector } from "react-redux";
import { getJobApplicationsState } from "../../slices/slice";
import { jobApplicationSliceAPI } from "../../slices/api";
import { useWrapQuery } from "@/core/hooks/api/useWrapQuery";

const SearchJobs: FC = () => {
  const jobsState = useSelector(getJobApplicationsState);

  console.log(jobsState);

  const params = new URLSearchParams();
  params.append("page", "0");
  params.append("limit", "5");

  const res = jobApplicationSliceAPI.useReadJobApplicationsQuery(
    params.toString()
  );

  useWrapQuery(res);

  return (
    <SearchBar
      {...{
        allowedTxtFields:
          searchJobsFieldsTxt as FormFieldTxtSearchBarT<SearchJobsFormT>[],
        resetVals: resetValsSearchJobs,
        filters: filtersSearchJobs,
        sorters: sortersSearchJobs,
      }}
    />
  );
};

export default SearchJobs;
