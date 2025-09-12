/** @jsxImportSource @emotion/react */
"use client";

import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import { JobApplicationT } from "@/features/jobApplications/types";
import type { FC } from "react";
import { btnsFooter } from "../../uiFactory/cards";
import BtnSvg from "@/common/components/buttons/BtnSvg";
import { formatDate } from "@/core/lib/dataStructure/formatters";
import LinkSvg from "@/common/components/links/LinkSvg";

type PropsType = {
  job: JobApplicationT;
};

const JobApplFooter: FC<PropsType> = ({ job }) => {
  const {
    ids: [ids],
  } = useGenIDs({ lengths: [2] });

  return (
    <div className="w-full flex justify-center items-center gap-8 flex-wrap">
      {btnsFooter.map((el, idx) => (
        <div key={ids[idx]} className="mx-auto">
          {!idx ? (
            <LinkSvg
              {...{
                act: "INFO",
                Svg: el.Svg,
                tooltipTxt: `Last Update: ${formatDate(job.updated_at)}`,
                href: `/job-applications/put/${job.id}`,
              }}
            />
          ) : (
            <BtnSvg
              {...{
                act: "ERR",
                Svg: el.Svg,
                tooltipTxt: "Delete",
              }}
            />
          )}
        </div>
      ))}
    </div>
  );
};

export default JobApplFooter;
