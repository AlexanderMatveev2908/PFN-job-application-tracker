/* eslint-disable @typescript-eslint/no-explicit-any */
import { FormFieldTxtT } from "@/common/types/ui";
import { FormFieldGen } from "@/core/uiFactory/classes";

const gen = new FormFieldGen();

export type PwdT = "password" | "confirm_password";

export const pwdFields: Record<PwdT, FormFieldTxtT<any>> = {
  password: gen.txtField({ name: "password" }),
  confirm_password: gen.txtField({ name: "confirm_password" }),
};
