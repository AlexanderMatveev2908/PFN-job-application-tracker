/** @jsxImportSource @emotion/react */
"use client";

import BtnSvg from "@/common/components/buttons/BtnSvg";
import { X } from "lucide-react";
import type { FC } from "react";
import { PayloadSetBarT } from "../../../context/etc/actions";

type PropsType = {
  setBar: (arg: PayloadSetBarT) => void;
};

const FilterBarHeader: FC<PropsType> = ({ setBar }) => {
  return (
    <div className="w-full grid grid-cols-2 border-b-2 border-neutral-800 items-center px-4 min-h-[60px]">
      <span className="txt__xl justify-self-start text-neutral-300">
        Filter
      </span>

      <div className="justify-self-end">
        <BtnSvg
          {...{
            Svg: X,
            act: "ERR",
            handleClick: () => setBar({ bar: "filterBar", val: false }),
          }}
        />
      </div>
    </div>
  );
};

export default FilterBarHeader;
