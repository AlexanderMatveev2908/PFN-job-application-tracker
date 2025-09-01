import { pwdSchema } from "@/core/paperwork";
import z from "zod";

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
