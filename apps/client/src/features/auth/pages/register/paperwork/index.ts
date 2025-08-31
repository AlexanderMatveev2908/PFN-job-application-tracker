import { REG_NAME } from "@/core/constants/regex";
import { emailSchema, pwdSchema } from "@/core/paperwork";
import { z } from "zod";
import {
  myMail,
  myPwd,
  wrapGetValsFormManualTest,
} from "@/features/auth/lib/etc";

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

export const resetValsRegister: RegisterFormT = {
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  confirm_password: "",
  terms: false,
};

export const getDefValsRegister = (): RegisterFormT =>
  wrapGetValsFormManualTest(resetValsRegister, {
    first_name: "Alex",
    last_name: "Matveev",
    email: myMail,
    password: myPwd,
    confirm_password: myPwd,
    terms: true,
  });
