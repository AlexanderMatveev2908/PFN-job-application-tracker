import z from "zod";
import { REG_PWD } from "../constants/regex";

export const emailSchema = z.object({
  email: z
    .email({ message: "Invalid email" })
    .min(1, "Email is required")
    .max(254, "Max length exceed"),
});

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
