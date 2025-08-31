import { FormFieldGen } from "@/core/uiFactory/classes";
import { EmailFormT } from "../paperwork";

const gen = new FormFieldGen<EmailFormT>();

export const emailField = gen.txtField({
  name: "email",
  type: "email",
});
