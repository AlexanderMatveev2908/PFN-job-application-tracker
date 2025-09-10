/* eslint-disable @typescript-eslint/no-explicit-any */
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
import { useSelector } from "react-redux";
import { getJobApplicationsState } from "../../slices/slice";
import { __cg } from "@/core/lib/log";
import WrapCSR from "@/common/components/wrappers/pages/WrapCSR";

type PropsType<K extends (...args: any) => any[]> = {
  hook: ReturnType<K>;
};

const SearchJobs = <K extends (...args: any) => any[]>({
  hook,
}: PropsType<K>) => {
  const jobsState = useSelector(getJobApplicationsState);

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_, res] = hook;

  __cg("jobs state", jobsState);

  return (
    <div className="w-full grid grid-cols-1 gap-10">
      <SearchBar
        {...{
          allowedTxtFields:
            searchJobsFieldsTxt as FormFieldTxtSearchBarT<SearchJobsFormT>[],
          resetVals: resetValsSearchJobs,
          filters: filtersSearchJobs,
          sorters: sortersSearchJobs,
          hook,
        }}
      />

      <WrapCSR
        {...{
          isLoading: res.isLoading,
        }}
      >
        <div className=""></div>
      </WrapCSR>
    </div>
  );
};

export default SearchJobs;
