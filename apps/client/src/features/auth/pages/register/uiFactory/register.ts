import { FormFieldGen } from "@/core/uiFactory/classes";
import { RegisterFormT } from "../schemas/register";
import { FormFieldTxtT } from "@/common/types/ui";

const gen = new FormFieldGen<RegisterFormT>();

export const registerSwap_0: FormFieldTxtT<RegisterFormT>[] = [
  gen.txtField({
    name: "first_name",
    required: true,
  }),
  gen.txtField({
    name: "last_name",
    required: true,
  }),
  gen.txtField({
    name: "email",
    required: true,
    type: "email",
  }),
];

export const registerSwap_1: FormFieldTxtT<RegisterFormT>[] = [
  gen.txtField({ name: "password", required: true }),
  gen.txtField({ name: "confirm_password", required: true }),
];
