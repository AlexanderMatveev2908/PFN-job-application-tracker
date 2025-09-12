/** @jsxImportSource @emotion/react */
"use client";

import {
  ApplicationStatusT,
  JobApplicationT,
} from "@/features/jobApplications/types";
import type { FC } from "react";
import { css } from "@emotion/react";
import JobApplMainInfo from "./components/JobApplMainInfo";
import JobApplSideInfo from "./components/JobApplSideInfo";
import JobApplFooter from "./components/JobApplFooter";

type PropsType = {
  job: JobApplicationT;
};

const statusClrMapper = {
  [ApplicationStatusT.APPLIED]: "neutral__500",
  [ApplicationStatusT.UNDER_REVIEW]: "blue__600",
  [ApplicationStatusT.INTERVIEW]: "blue__300",
  [ApplicationStatusT.OFFER]: "green__600",
  [ApplicationStatusT.REJECTED]: "red__600",
  [ApplicationStatusT.WITHDRAWN]: "yellow__600",
};

const JobApplItem: FC<PropsType> = ({ job }) => {
  const suffix = statusClrMapper[job.status];

  return (
    <div
      data-testid={`job_appl__card`}
      className="w-full grid grid-cols-1 border-3 p-5 rounded-xl gap-6"
      css={css`
        border-color: var(--${suffix});
      `}
    >
      <JobApplMainInfo {...{ job }} />

      <JobApplSideInfo {...{ job }} />

      <JobApplFooter {...{ job, suffix }} />
    </div>
  );
};

export default JobApplItem;
