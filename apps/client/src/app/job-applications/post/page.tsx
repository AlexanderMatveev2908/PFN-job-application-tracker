/* eslint-disable @typescript-eslint/no-explicit-any */
/** @jsxImportSource @emotion/react */
"use client";

import JobApplicationForm from "@/features/jobApplications/forms/JobApplicationForm/JobApplicationForm";
import {
  addJobApplicationSchema,
  resetValsJobApplForm,
} from "@/features/jobApplications/forms/JobApplicationForm/paperwork/jobAppliication";
import { zodResolver } from "@hookform/resolvers/zod";
import type { FC } from "react";
import { FormProvider, useFieldArray, useForm } from "react-hook-form";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { jobApplicationSliceAPI } from "@/features/jobApplications/slices/api";
import { genFormData, logFormErrs } from "@/core/lib/forms";
import { useAppFormsCtxConsumer } from "@/core/contexts/appForms/hooks/useAppFormsCtxConsumer";
import { positionNameField } from "@/features/jobApplications/uiFactory";

const Page: FC = () => {
  const formCtx = useForm({
    mode: "onChange",
    resolver: zodResolver(addJobApplicationSchema) as any,
    defaultValues: resetValsJobApplForm,
  });
  const { handleSubmit, reset } = formCtx;

  const { formCtxJobs: formCtxRead } = useAppFormsCtxConsumer();
  const { control: controlRead } = formCtxRead;
  const { append } = useFieldArray({
    control: controlRead,
    name: "txtFields",
  });

  const { nav, wrapAPI } = useKitHooks();
  const [mutate] = jobApplicationSliceAPI.useAddJobApplicationMutation();

  const handleSave = handleSubmit(async (data) => {
    const formData = genFormData(data);

    const res = await wrapAPI({
      cbAPI: () => mutate(formData),
    });

    if (!res) return;

    reset(resetValsJobApplForm);

    append({ ...positionNameField, val: "" });

    formCtxRead.setValue("txtFields.0.val", res.job_application.company_name, {
      shouldValidate: true,
    });
    formCtxRead.setValue("txtFields.1.val", res.job_application.position_name, {
      shouldValidate: true,
    });

    nav.replace("/job-applications/read");
  }, logFormErrs);

  return (
    <FormProvider {...formCtx}>
      <JobApplicationForm {...{ handleSave }} />
    </FormProvider>
  );
};

export default Page;
