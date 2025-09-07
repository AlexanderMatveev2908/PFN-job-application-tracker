/** @jsxImportSource @emotion/react */
"use client";

import JobApplicationForm from "@/features/jobApplications/forms/JobApplicationForm/JobApplicationForm";
import { logFormErrs } from "@/core/lib/etc";
import { __cg } from "@/core/lib/log";
import {
  addJobApplicationSchema,
  ApplicationStatusT,
} from "@/features/jobApplications/forms/JobApplicationForm/paperwork/jobAppliication";
import { zodResolver } from "@hookform/resolvers/zod";
import type { FC } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { defValDatePicker } from "@/core/lib/formatters";

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

  const handleSave = handleSubmit(async (data) => {
    __cg(data);
  }, logFormErrs);

  return (
    <FormProvider {...formCtx}>
      <JobApplicationForm {...{ handleSave }} />
    </FormProvider>
  );
};

export default Page;
