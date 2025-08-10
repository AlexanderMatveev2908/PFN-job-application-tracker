import { REG_NAME } from "@/core/constants/regex";
import { z } from "zod";

export const registerSchema = z.object({
  first_name: z
    .string()
    .min(1, "First Name is required")
    .max(50, "Max length exceeded")
    .regex(REG_NAME, "Invalid characters"),
});

export type RegisterFormT = z.infer<typeof registerSchema>;
