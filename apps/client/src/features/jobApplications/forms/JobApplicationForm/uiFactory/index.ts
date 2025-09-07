import { FormFieldGen } from "@/core/uiFactory/classes";
import { JobApplicationFormT } from "@/features/jobApplications/paperwork";

const gen = new FormFieldGen<JobApplicationFormT>();

const companyNameField = gen.txtField({ name: "company_name" });
const positionNameField = gen.txtField({ name: "position_name" });
const notesField = gen.txtField({ name: "notes" });

export const txtFieldsApplicationForm = [
  companyNameField,
  positionNameField,
  notesField,
];

export const statusField = gen.checkField({
  label: "Status Application",
  name: "status",
  type: "checkbox",
});
