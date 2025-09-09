import { REG_JOB_NAME } from "@/core/constants/regex";
import { parseDevValUsFriendly } from "@/core/lib/dataStructure/formatters";
import { MapperArrayFieldsT, txtFieldSchema } from "@/core/paperwork";
import z from "zod";
import { searchJobsFieldsTxt } from "../uiFactory";
import { ApplicationStatusT } from "../../../types";

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

    status: z.array(z.enum(Object.values(ApplicationStatusT))),
  })
  .superRefine((data, ctx) => {
    let i = 0;

    while (i < data.txtFields.length) {
      const curr = data.txtFields?.[i];
      const friendlyName = parseDevValUsFriendly(curr.name, {});

      if (curr.val.trim().length)
        if (!mapper[curr.name as keyof typeof mapper].reg.test(curr.val))
          ctx.addIssue({
            code: "custom",
            message: `Invalid ${friendlyName}`,
            path: [`txtFields.${i}.val`],
          });
        else if (curr.val.length > mapper[curr.name as keyof typeof mapper].max)
          ctx.addIssue({
            code: "custom",
            message: `${friendlyName} length exceeded`,
            path: [`txtFields.${i}.val`],
          });

      i++;
    }
  });

export type SearchJobsFormT = z.infer<typeof searchJobsSchema>;

export const resetValsSearchJobs: SearchJobsFormT = {
  txtFields: [{ ...searchJobsFieldsTxt[0], val: "" }],
  status: [],
};
