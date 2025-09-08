import { REG_JOB_NAME } from "@/core/constants/regex";
import { MapperArrayFieldsT, txtFieldSchema } from "@/core/paperwork";
import z from "zod";

const mapper: MapperArrayFieldsT = {
  company_name: {
    reg: REG_JOB_NAME,
    max: 100,
  },
  position_name: {
    reg: REG_JOB_NAME,
    max: 100,
  },
};

export const searchJobsSchema = z
  .object({
    txtFields: z.array(txtFieldSchema),
  })
  .superRefine((data, ctx) => {
    let i = 0;

    do {
      const curr = data.txtFields?.[i];
      if (curr.val.trim().length)
        if (!mapper[curr.name as keyof typeof mapper].reg.test(curr.val))
          ctx.addIssue({
            code: "custom",
            message: `Invalid ${curr.name}`,
            path: [`txtFields.${i}.val`],
          });
        else if (curr.val.length > mapper[curr.name as keyof typeof mapper].max)
          ctx.addIssue({
            code: "custom",
            message: `${curr.name} length exceeded`,
            path: [`txtFields.${i}.val`],
          });

      i++;
    } while (i < data.txtFields.length);
  });

export type SearchJobsFormT = z.infer<typeof searchJobsSchema>;
