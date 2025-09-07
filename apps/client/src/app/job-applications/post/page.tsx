/** @jsxImportSource @emotion/react */
"use client";

import JobApplicationForm from "@/features/jobApplications/forms/JobApplicationForm/JobApplicationForm";
import {
  addJobApplicationSchema,
  resetValsJobApplForm,
} from "@/features/jobApplications/forms/JobApplicationForm/paperwork/jobAppliication";
import { zodResolver } from "@hookform/resolvers/zod";
import type { FC } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { jobApplicationSliceAPI } from "@/features/jobApplications/slices/api";
import { genFormData, logFormErrs } from "@/core/lib/forms";

const Page: FC = () => {
  const formCtx = useForm({
    mode: "onChange",
    resolver: zodResolver(addJobApplicationSchema),
    defaultValues: resetValsJobApplForm,
  });
  const { handleSubmit, reset } = formCtx;

  const { nav, wrapAPI } = useKitHooks();
  const [mutate] = jobApplicationSliceAPI.useAddJobApplicationMutation();

  const handleSave = handleSubmit(async (data) => {
    const formData = genFormData(data);

    const res = await wrapAPI({
      cbAPI: () => mutate(formData),
    });

    if (!res) return;

    reset(resetValsJobApplForm);

    nav.replace("/job-applications/read");
  }, logFormErrs);

  return (
    <FormProvider {...formCtx}>
      <JobApplicationForm {...{ handleSave }} />
    </FormProvider>
  );
};

export default Page;
