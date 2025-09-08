import { FormFieldGen } from "@/core/uiFactory/classes";
import { JobApplicationFormT } from "@/features/jobApplications/forms/JobApplicationForm/paperwork/jobAppliication";
import {
  companyNameField,
  positionNameField,
} from "@/features/jobApplications/uiFactory";

const gen = new FormFieldGen<JobApplicationFormT>();

const notesField = gen.txtField({ name: "notes", type: "textarea" });

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
