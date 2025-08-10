import { FormFieldGen } from "@/core/uiFactory/classes";
import { RegisterFormT } from "../schemas/register";

const gen = new FormFieldGen<RegisterFormT>();

export const registerSwap_0 = [
  gen.txtField({
    name: "last_name",
    required: true,
  }),
  gen.txtField({
    name: "first_name",
    required: true,
  }),
  gen.txtField({
    name: "email",
    required: true,
    type: "email",
  }),
];
