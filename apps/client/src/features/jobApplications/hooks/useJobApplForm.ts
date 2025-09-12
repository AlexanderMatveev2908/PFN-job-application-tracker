/* eslint-disable @typescript-eslint/no-explicit-any */
import { zodResolver } from "@hookform/resolvers/zod";
import { useFieldArray, useForm } from "react-hook-form";
import {
  addJobApplicationSchema,
  resetValsJobApplForm,
} from "../forms/JobApplicationForm/paperwork/jobAppliication";
import { useAppFormsCtxConsumer } from "@/core/contexts/appForms/hooks/useAppFormsCtxConsumer";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { genFormData, logFormErrs } from "@/core/lib/forms";
import { TriggerApiT } from "@/common/types/api";
import { positionNameField } from "../uiFactory";

type Params<T extends Record<string, any>> = {
  mutate: TriggerApiT<T>;
};

export const useJobApplForm = <T extends Record<string, any>>({
  mutate,
}: Params<T>) => {
  const formCtx = useForm({
    mode: "onChange",

    resolver: zodResolver(addJobApplicationSchema) as any,
    defaultValues: resetValsJobApplForm,
  });
  const { handleSubmit, reset } = formCtx;

  const { formCtxJobs: formCtxRead } = useAppFormsCtxConsumer();
  const { control: controlRead } = formCtxRead;
  const { append: appendReadForm } = useFieldArray({
    control: controlRead,
    name: "txtFields",
  });

  const { nav, wrapAPI } = useKitHooks();

  const handleSave = handleSubmit(async (data) => {
    const formData = genFormData(data);

    const res = await wrapAPI<T>({
      cbAPI: () => mutate(formData),
    });

    if (!res) return;

    reset(resetValsJobApplForm);

    appendReadForm({ ...positionNameField, val: "" });

    formCtxRead.setValue("txtFields.0.val", res.job_application.company_name, {
      shouldValidate: true,
    });
    formCtxRead.setValue("txtFields.1.val", res.job_application.position_name, {
      shouldValidate: true,
    });

    nav.replace("/job-applications/read");
  }, logFormErrs);

  return {
    handleSave,
    formCtx,
  };
};
