/** @jsxImportSource @emotion/react */
"use client";

import { FormFieldTxtSearchBarT } from "@/common/types/ui";
import {
  resetValsSearchJobs,
  SearchJobsFormT,
  searchJobsSchema,
} from "@/features/jobApplications/paperwork/searchJobs";
import { searchJobsFieldsTxt } from "@/features/jobApplications/uiFactory/searchJobs";
import SearchBar from "@/features/layout/components/SearchBar/SearchBar";
import { zodResolver } from "@hookform/resolvers/zod";
import type { FC } from "react";
import { FormProvider, useForm } from "react-hook-form";

const Page: FC = () => {
  const formCtx = useForm<SearchJobsFormT>({
    mode: "onChange",
    resolver: zodResolver(searchJobsSchema),
    defaultValues: resetValsSearchJobs,
  });

  return (
    <div className="page__shape">
      <FormProvider {...formCtx}>
        <SearchBar
          {...{
            allowedTxtFields:
              searchJobsFieldsTxt as FormFieldTxtSearchBarT<SearchJobsFormT>[],
            resetVals: resetValsSearchJobs,
          }}
        />
      </FormProvider>
    </div>
  );
};

export default Page;
