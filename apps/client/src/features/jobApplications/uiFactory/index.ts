import { FormFieldGen } from "@/core/uiFactory/classes";

const gen = new FormFieldGen();

export const companyNameField = gen.txtField({ name: "company_name" });
export const positionNameField = gen.txtField({ name: "position_name" });
