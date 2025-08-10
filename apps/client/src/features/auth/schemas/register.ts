import { REG_NAME, REG_PWD } from "@/core/constants/regex";
import { z } from "zod";

export const registerSchema = z
  .object({
    first_name: z
      .string()
      .min(1, "First Name is required")
      .max(50, "Max length exceeded")
      .regex(REG_NAME, "Invalid characters"),
    last_name: z
      .string()
      .min(1, "Last Name is required")
      .max(50, "Max length exceeded")
      .regex(REG_NAME, "Invalid characters"),

    email: z
      .email({ message: "Invalid email" })
      .min(1, "Email is required")
      .max(100, "Max length exceed"),

    pwd: z
      .string()
      .min(1, "Password required")
      .max(100, "Max length exceeded")
      .regex(REG_PWD, "Invalid password"),
    confirm_pwd: z.string(),

    terms: z.literal(true, { message: "You must accept terms & conditions" }),
  })
  .superRefine((data, ctx) => {
    if (data.pwd !== data.confirm_pwd)
      ctx.addIssue({
        code: "custom",
        message: "Passwords do not match",
        path: ["confirm_pwd"],
      });
  });

export type RegisterFormT = z.infer<typeof registerSchema>;
