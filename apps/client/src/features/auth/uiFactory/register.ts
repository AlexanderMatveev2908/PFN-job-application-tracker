import { FormFieldGen } from "@/core/uiFactory/formFields";
import { RegisterFormT } from "../schemas/register";

const gen = new FormFieldGen<RegisterFormT>();

export const registerField = gen.txtField({
  label: "First Name",
  name: "first_name",
  required: true,
});
