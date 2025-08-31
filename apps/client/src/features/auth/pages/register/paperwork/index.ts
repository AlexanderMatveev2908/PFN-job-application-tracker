import { REG_NAME } from "@/core/constants/regex";
import { emailSchema, pwdSchema } from "@/core/paperwork";
import { z } from "zod";

export const registerSchema = emailSchema
  .extend({
    first_name: z
      .string()
      .min(1, "First Name is required")
      .max(100, "Max length exceeded")
      .regex(REG_NAME, "Invalid characters"),
    last_name: z
      .string()
      .min(1, "Last Name is required")
      .max(100, "Max length exceeded")
      .regex(REG_NAME, "Invalid characters"),

    confirm_password: z
      .string({ error: "You must confirm password" })
      .min(1, "You must confirm password"),

    terms: z
      .boolean()
      .refine((v) => v, { message: "You must accept terms & conditions" }),
  })
  .and(pwdSchema)
  .refine((d) => d.password === d.confirm_password, {
    path: ["confirm_password"],
    message: "Passwords do not match",
  });

export type RegisterFormT = z.infer<typeof registerSchema>;
