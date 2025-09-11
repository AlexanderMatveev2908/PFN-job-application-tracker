/** @jsxImportSource @emotion/react */
"use client";

import { JobApplicationT } from "@/features/jobApplications/types";
import type { FC } from "react";
import { genCardPairs } from "../uiFactory";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import PairTxtSvg from "@/common/components/elements/PairTxtSvg";

type PropsType = {
  job: JobApplicationT;
};

const JobApplItem: FC<PropsType> = ({ job: el }) => {
  const {
    ids: [ids],
  } = useGenIDs({ lengths: [2] });

  return (
    <div className="w-full grid grid-cols-1 border-3 border-neutral-300 p-5 rounded-xl gap-6">
      {genCardPairs(el).map((pair, i) => (
        <PairTxtSvg
          key={ids[i]}
          {...{
            el: {
              label: pair.val as string,
              Svg: pair.Svg,
            },
          }}
        />
      ))}
    </div>
  );
};

export default JobApplItem;
