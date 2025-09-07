import { SqlTableRoot } from "@/common/types/db";
import { parseDevValUsFriendly } from "@/core/lib/dataStructure/formatters";

export enum ApplicationStatusT {
  APPLIED = "APPLIED",
  UNDER_REVIEW = "UNDER_REVIEW",
  INTERVIEW = "INTERVIEW",
  OFFER = "OFFER",
  REJECTED = "REJECTED",
  WITHDRAWN = "WITHDRAWN",
}

export const applicationStatusChoices = Object.values(ApplicationStatusT).map(
  (v) => ({
    val: v,
    label: parseDevValUsFriendly(v),
  })
);

export interface JobApplicationT extends SqlTableRoot {
  company_name: string;
  user_id: string;
  position_name: string;
  status: ApplicationStatusT;
  date_applied: string;
}
