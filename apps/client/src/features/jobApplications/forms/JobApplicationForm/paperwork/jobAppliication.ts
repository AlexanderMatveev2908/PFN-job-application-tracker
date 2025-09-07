import { REG_DATE_PICKER, REG_NAME, REG_TXT } from "@/core/constants/regex";
import { parseDevValUsFriendly } from "@/core/lib/formatters";
import z from "zod";

export enum ApplicationStatusT {
  APPLIED = "APPLIED",
  UNDER_REVIEW = "UNDER_REVIEW",
  INTERVIEW = "INTERVIEW",
  OFFER = "OFFER",
  REJECTED = "REJECTED",
  WITHDRAWN = "WITHDRAWN",
}

export const applicationStatusChoices = Object.values(ApplicationStatusT).map(
  (v) => ({
    val: v,
    label: parseDevValUsFriendly(v),
  })
);

export const addJobApplicationSchema = z.object({
  company_name: z
    .string()
    .min(1, "Company name required")
    .max(100, "Max length exceeded")
    .regex(REG_NAME, "Invalid company name"),

  position_name: z
    .string()
    .min(1, "Position name required")
    .max(100, "Max length exceeded")
    .regex(REG_NAME, "Invalid position name"),

  notes: z
    .string()
    .regex(REG_TXT, "Invalid notes characters")
    .max(1000, "Max length exceeded")
    .optional(),

  date_applied: z
    .string()
    .regex(REG_DATE_PICKER, "Invalid date format")
    .refine((v) => {
      const d = new Date(v);

      return !isNaN(d.getTime()) && d.toISOString().split("T")[0] === v;
    }, "Invalid date"),

  status: z
    .preprocess(
      (val) => (!val ? undefined : val),
      z
        .enum(Object.values(ApplicationStatusT), {
          error: "Invalid application status",
        })
        .optional()
    )
    .refine((v) => !!v, { message: "Status required" }),
});

export type JobApplicationFormT = z.infer<typeof addJobApplicationSchema>;
