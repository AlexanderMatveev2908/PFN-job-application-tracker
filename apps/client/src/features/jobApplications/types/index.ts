import { parseDevValUsFriendly } from "@/core/lib/formatters";

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
