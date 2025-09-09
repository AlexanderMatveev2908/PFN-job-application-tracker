/** @jsxImportSource @emotion/react */
"use client";

import SearchJobs from "@/features/jobApplications/pages/SearchJobs/SearchJobs";
import {
  resetValsSearchJobs,
  SearchJobsFormT,
  searchJobsSchema,
} from "@/features/jobApplications/pages/SearchJobs/paperwork";
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

  return (
    <div className="page__shape">
      <SearchBarWrapper {...{ formCtx }}>
        <SearchJobs />
      </SearchBarWrapper>
    </div>
  );
};

export default Page;
