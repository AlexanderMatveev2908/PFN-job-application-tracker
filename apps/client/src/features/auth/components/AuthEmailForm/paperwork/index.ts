import { emailSchema } from "@/core/paperwork";
import z from "zod";

export type EmailFormT = z.infer<typeof emailSchema>;
