import { REG_NAME, REG_TXT } from "@/core/constants/regex";
import z from "zod";

export enum ApplicationStatusT {
  APPLIED = "APPLIED",
  UNDER_REVIEW = "UNDER_REVIEW",
  INTERVIEW = "INTERVIEW",
  OFFER = "OFFER",
  REJECTED = "REJECTED",
  WITHDRAWN = "WITHDRAWN",
}

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
    .number()
    .int()
    .nonnegative("Value must be a positive integer")
    .optional()
    .default(() => Date.now()),

  status: z.enum(
    Object.values(ApplicationStatusT),
    "Invalid application status"
  ),
});

export type JobApplicationFormT = z.infer<typeof addJobApplicationSchema>;
