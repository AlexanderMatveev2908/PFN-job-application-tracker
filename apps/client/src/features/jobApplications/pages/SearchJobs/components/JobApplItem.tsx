/** @jsxImportSource @emotion/react */
"use client";

import { JobApplicationT } from "@/features/jobApplications/types";
import type { FC } from "react";
import { genPairsMainCardInfo, genPairsSecondaryInfoCard } from "../uiFactory";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import PairTxtSvg from "@/common/components/elements/PairTxtSvg";
import BtnSvg from "@/common/components/buttons/BtnSvg";
import DropMenuAbsolute from "@/common/components/dropMenus/DropMenuAbsolute";
import { css } from "@emotion/react";
import { TbNotes } from "react-icons/tb";

type PropsType = {
  job: JobApplicationT;
};

const JobApplItem: FC<PropsType> = ({ job }) => {
  const { ids } = useGenIDs({ lengths: [4, 2] });

  return (
    <div className="w-full grid grid-cols-1 border-3 border-neutral-300 p-5 rounded-xl gap-6">
      {genPairsMainCardInfo(job).map((pair, i) => (
        <PairTxtSvg
          key={ids[0][i]}
          {...{
            el: {
              label: pair.val as string,
              Svg: pair.Svg,
            },
          }}
        />
      ))}

      <div className="w-[250px]">
        <DropMenuAbsolute
          {...{
            el: {
              Svg: TbNotes,
              label: "Notes",
            },
            $cstmBtnCSS: css`
              padding: 5px 20px;
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
  );
};

export default JobApplItem;
