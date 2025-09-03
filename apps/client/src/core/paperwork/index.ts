import z from "zod";
import { REG_PWD } from "../constants/regex";

export const emailSchema = z.object({
  email: z
    .email({ message: "Invalid email" })
    .min(1, "Email is required")
    .max(254, "Max length exceed"),
});

export type EmailFormT = z.infer<typeof emailSchema>;

export const resetValsEmailForm: EmailFormT = {
  email: "",
};

export const pwdSchema = z.object({
  password: z
    .string({ error: "Password required" })
    .min(1, "Password required")
    .max(100, "Max length exceeded")
    .regex(REG_PWD, "Invalid password"),
});

export type PwdFormT = z.infer<typeof pwdSchema>;

export const resetValsPwdForm: PwdFormT = {
  password: "",
};

export const pwdsSchema = z
  .object({
    confirm_password: z
      .string({ error: "You must confirm password" })
      .min(1, "You must confirm password"),
  })
  .and(pwdSchema)
  .refine((d) => d.password === d.confirm_password, {
    path: ["confirm_password"],
    message: "Passwords do not match",
  });

export type PwdsFormT = z.infer<typeof pwdsSchema>;

export const resetValsPwdsForm: PwdsFormT = {
  password: "",
  confirm_password: "",
};
