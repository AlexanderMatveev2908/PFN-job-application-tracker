import { FormFieldGen } from "@/core/uiFactory/classes";
import { RegisterFormT } from "../schemas/register";
import { FormFieldCheckT, FormFieldTxtT } from "@/common/types/ui";

const gen = new FormFieldGen<RegisterFormT>();

export const registerSwap_0: FormFieldTxtT<RegisterFormT>[] = [
  gen.txtField({
    name: "first_name",
  }),
  gen.txtField({
    name: "last_name",
  }),
  gen.txtField({
    name: "email",
    type: "email",
  }),
];

export const registerSwap_1: FormFieldTxtT<RegisterFormT>[] = [
  gen.txtField({ name: "password" }),
  gen.txtField({ name: "confirm_password" }),
];

export const termsField: FormFieldCheckT<RegisterFormT> = gen.checkField({
  name: "terms",
});
