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
import { getJobList } from "../../slices/slice";
import JobApplItem from "./components/JobApplItem";

type PropsType<K extends any[]> = {
  hook: K;
  schema: ZodObject;
};

const SearchJobs = <K extends any[]>({ hook, schema }: PropsType<K>) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_, res] = hook;
  const isPending = res?.isLoading || res?.isFetching || res?.isUninitialized;

  const jobs = useSelector(getJobList);

  return (
    <div className="w-full grid grid-cols-1 gap-14">
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
          isLoading: isPending,
          $minH: "min-h-[60vh]",
        }}
      >
        <div className="w-full grid grid-cols-1 lg:grid-cols-2 gap-10 pb-[100px]">
          {jobs.map((el) => (
            <JobApplItem key={el.id} {...{ job: el }} />
          ))}
        </div>
      </WrapCSR>
    </div>
  );
};

export default SearchJobs;
