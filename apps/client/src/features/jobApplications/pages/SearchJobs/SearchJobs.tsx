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
import WrapCSR from "@/common/components/wrappers/pages/WrapCSR";
import { ZodObject } from "zod";
import { useSelector } from "react-redux";
import { getJobApplicationsState } from "../../slices/slice";

type PropsType<K extends any[]> = {
  hook: K;
  schema: ZodObject;
};

const SearchJobs = <K extends any[]>({ hook, schema }: PropsType<K>) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_, res] = hook;

  const jobsState = useSelector(getJobApplicationsState);

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
          schema,
        }}
      />

      <WrapCSR
        {...{
          isLoading: res.isLoading || res?.isFetching,
          $minH: "min-h-[75vh]",
        }}
      >
        <div className=""></div>
      </WrapCSR>
    </div>
  );
};

export default SearchJobs;
