/** @jsxImportSource @emotion/react */
"use client";

import JobApplicationForm from "@/features/jobApplications/forms/JobApplicationForm/JobApplicationForm";
import { logFormErrs } from "@/core/lib/etc";
import { addJobApplicationSchema } from "@/features/jobApplications/forms/JobApplicationForm/paperwork/jobAppliication";
import { zodResolver } from "@hookform/resolvers/zod";
import type { FC } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { defValDatePicker, genFormData } from "@/core/lib/formatters";
import { ApplicationStatusT } from "@/features/jobApplications/types";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { jobApplicationSliceAPI } from "@/features/jobApplications/slices/api";

const Page: FC = () => {
  const formCtx = useForm({
    mode: "onChange",
    resolver: zodResolver(addJobApplicationSchema),
    defaultValues: {
      company_name: "",
      position_name: "",
      notes: "",
      date_applied: defValDatePicker(),
      status: "" as ApplicationStatusT,
    },
  });
  const { handleSubmit } = formCtx;

  const { nav, wrapAPI } = useKitHooks();
  const [mutate] = jobApplicationSliceAPI.useAddJobApplicationMutation();

  const handleSave = handleSubmit(async (data) => {
    const formData = genFormData(data);

    const res = await wrapAPI({
      cbAPI: () => mutate(formData),
    });
  }, logFormErrs);

  return (
    <FormProvider {...formCtx}>
      <JobApplicationForm {...{ handleSave }} />
    </FormProvider>
  );
};

export default Page;
