import { FormFieldGen } from "@/core/uiFactory/classes";
import { JobApplicationFormT } from "@/features/jobApplications/forms/JobApplicationForm/paperwork/jobAppliication";

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
  type: "radio",
});

export const dateApplicationField = gen.txtField({
  name: "date_applied",
  type: "date",
});
