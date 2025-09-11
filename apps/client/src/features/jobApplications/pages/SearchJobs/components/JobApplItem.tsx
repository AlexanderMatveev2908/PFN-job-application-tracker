/** @jsxImportSource @emotion/react */
"use client";

import {
  ApplicationStatusT,
  JobApplicationT,
} from "@/features/jobApplications/types";
import type { FC } from "react";
import { genPairsMainCardInfo, genPairsSecondaryInfoCard } from "../uiFactory";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import PairTxtSvg from "@/common/components/elements/PairTxtSvg";
import BtnSvg from "@/common/components/buttons/BtnSvg";
import DropMenuAbsolute from "@/common/components/dropMenus/DropMenuAbsolute";
import { css } from "@emotion/react";
import { TbNotes } from "react-icons/tb";
import { IoStatsChart } from "react-icons/io5";

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
  const { ids } = useGenIDs({ lengths: [4, 2] });

  const suffix = statusClrMapper[job.status];

  return (
    <div
      className="w-full grid grid-cols-1 border-3 p-5 rounded-xl gap-6"
      css={css`
        border-color: var(--${suffix});
      `}
    >
      {genPairsMainCardInfo(job).map((pair, i) => (
        <PairTxtSvg
          key={ids[0][i]}
          {...{
            el: {
              label: pair.val as string,
              Svg: pair.Svg,
            },
            $justify: "start",
          }}
        />
      ))}

      <div
        className="w-full grid gap-6 justify-items-center"
        css={css`
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        `}
      >
        <div className="w-fit">
          <DropMenuAbsolute
            {...{
              el: {
                Svg: TbNotes,
                label: "Notes",
              },
              $cstmBtnCSS: css`
                padding: 5px 40px;
              `,
            }}
          >
            {() => (
              <div className="flex justify-center p-3">
                <span className="txt__md"> {job.notes ?? "N/A"}</span>
              </div>
            )}
          </DropMenuAbsolute>
        </div>

        <div className="w-full grid grid-cols-2 justify-items-center">
          {genPairsSecondaryInfoCard(job).map((pair, i) => (
            <BtnSvg
              key={ids[1][i]}
              {...{
                Svg: pair.Svg,
                tooltipTxt: pair.val,
                $SvgSize: "sm",
              }}
            />
          ))}
        </div>
      </div>

      <div
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
          }}
        />
      </div>
    </div>
  );
};

export default JobApplItem;
