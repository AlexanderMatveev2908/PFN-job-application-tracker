import { REG_NAME, REG_PWD } from "@/core/constants/regex";
import { z } from "zod";

export const registerSchema = z
  .object({
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

    email: z
      .email({ message: "Invalid email" })
      .min(1, "Email is required")
      .max(254, "Max length exceed"),

    password: z
      .string({ error: "Password required" })
      .min(1, "Password required")
      .max(100, "Max length exceeded")
      .regex(REG_PWD, "Invalid password"),
    confirm_password: z
      .string({ error: "You must confirm password" })
      .min(1, "You must confirm password"),

    terms: z
      .boolean()
      .refine((v) => v, { message: "You must accept terms & conditions" }),
  })
  .refine((d) => d.password === d.confirm_password, {
    path: ["confirm_password"],
    message: "Passwords do not match",
  });

export type RegisterFormT = z.infer<typeof registerSchema>;
