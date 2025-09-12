/** @jsxImportSource @emotion/react */
"use client";

import JobApplicationForm from "@/features/jobApplications/forms/JobApplicationForm/JobApplicationForm";
import { useJobApplForm } from "@/features/jobApplications/hooks/useJobApplForm";
import { jobApplicationSliceAPI } from "@/features/jobApplications/slices/api";
import type { FC } from "react";
import { FormProvider } from "react-hook-form";

const Page: FC = () => {
  const [mutate] = jobApplicationSliceAPI.usePutJobApplicationMutation();

  const { handleSave, formCtx } = useJobApplForm({ mutate });

  return (
    <FormProvider {...formCtx}>
      <JobApplicationForm {...{ handleSave }} />
    </FormProvider>
  );
};

export default Page;
