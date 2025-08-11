/** @jsxImportSource @emotion/react */
"use client";

import BtnShim from "@/common/components/buttons/BtnShim/BtnShim";
import BtnsSwapper from "@/common/components/HOC/BtnsSwapper";
import type { Dispatch, FC, SetStateAction } from "react";

type PropsType = {
  currSwap: number;
  setCurrSwap: Dispatch<SetStateAction<number>>;
};

const FooterForm: FC<PropsType> = ({ currSwap, setCurrSwap }) => {
  return (
    <div className="w-full grid grid-cols-1 gap-14 p-5">
      <BtnsSwapper
        {...{
          currSwap,
          setCurrSwap,
          totSwaps: 2,
        }}
      />

      <div className="w-[250px] justify-self-center">
        <BtnShim
          {...{
            type: "submit",
            label: "Submit",
          }}
        />
      </div>
    </div>
  );
};

export default FooterForm;
