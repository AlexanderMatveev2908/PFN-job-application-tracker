/** @jsxImportSource @emotion/react */
"use client";

import SearchJobs from "@/features/jobApplications/pages/SearchJobs/SearchJobs";
import {
  resetValsSearchJobs,
  SearchJobsFormT,
  searchJobsSchema,
} from "@/features/jobApplications/pages/SearchJobs/paperwork";
import { jobApplicationSliceAPI } from "@/features/jobApplications/slices/api";
import SearchBarWrapper from "@/features/layout/components/SearchBar/sideComponents/SearchBarWrapper";
import { zodResolver } from "@hookform/resolvers/zod";
import type { FC } from "react";
import { useForm } from "react-hook-form";

const Page: FC = () => {
  const formCtx = useForm<SearchJobsFormT>({
    mode: "onChange",
    resolver: zodResolver(searchJobsSchema),
    defaultValues: resetValsSearchJobs,
  });

  const hook = jobApplicationSliceAPI.useLazyReadJobApplicationsQuery();

  return (
    <div className="page__shape">
      <SearchBarWrapper<
        SearchJobsFormT,
        typeof jobApplicationSliceAPI.useLazyReadJobApplicationsQuery
      >
        {...{ formCtx, hook, schema: searchJobsSchema }}
      >
        {(arg) => <SearchJobs {...arg} />}
      </SearchBarWrapper>
    </div>
  );
};

export default Page;
