/** @jsxImportSource @emotion/react */
"use client";

import DropMenuAbsolute from "@/common/components/dropMenus/DropMenuAbsolute";
import { css } from "@emotion/react";
import type { FC } from "react";
import { TbNotes } from "react-icons/tb";
import { genPairsSecondaryInfoCard } from "../../uiFactory";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import BtnSvg from "@/common/components/buttons/BtnSvg";
import { JobApplicationT } from "@/features/jobApplications/types";

type PropsType = {
  job: JobApplicationT;
};

const JobApplSideInfo: FC<PropsType> = ({ job }) => {
  const { ids } = useGenIDs({ lengths: [2] });

  return (
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
              <span data-testid={"card__notes"} className="txt__md">
                {" "}
                {job.notes ?? "N/A"}
              </span>
            </div>
          )}
        </DropMenuAbsolute>
      </div>

      <div className="w-full grid grid-cols-2 justify-items-center">
        {genPairsSecondaryInfoCard(job).map((pair, i) => (
          <BtnSvg
            key={ids[0][i]}
            {...{
              Svg: pair.Svg,
              tooltipTxt: pair.val,
              $SvgSize: "sm",
            }}
          />
        ))}
      </div>
    </div>
  );
};

export default JobApplSideInfo;
