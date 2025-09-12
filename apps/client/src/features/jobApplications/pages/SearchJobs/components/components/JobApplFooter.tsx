/** @jsxImportSource @emotion/react */
"use client";

import PairTxtSvg from "@/common/components/elements/PairTxtSvg";
import { JobApplicationT } from "@/features/jobApplications/types";
import { css } from "@emotion/react";
import type { FC } from "react";
import { IoStatsChart } from "react-icons/io5";

type PropsType = {
  job: JobApplicationT;
  suffix: string;
};

const JobApplFooter: FC<PropsType> = ({ job, suffix }) => {
  return (
    <div
      data-testid={"job_appl__card__status"}
      className="mx-auto border-2 rounded-xl py-2 px-10"
      css={css`
        color: var(--${suffix});
      `}
    >
      <PairTxtSvg
        {...{
          el: {
            Svg: IoStatsChart,
            label: job.status,
          },
          testID: "card__status",
        }}
      />
    </div>
  );
};

export default JobApplFooter;
