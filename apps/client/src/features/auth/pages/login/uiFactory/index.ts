import { FormFieldGen } from "@/core/uiFactory/classes";
import { LoginFormT } from "../paperwork";

const gen = new FormFieldGen<LoginFormT>();

export const mailField = gen.txtField({
  name: "email",
  type: "email",
});
export const pwdField = gen.txtField({
  name: "password",
});
