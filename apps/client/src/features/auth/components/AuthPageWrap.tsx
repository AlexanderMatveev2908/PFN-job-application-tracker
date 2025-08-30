/** @jsxImportSource @emotion/react */
"use client";

import ProgressSwap from "@/common/components/elements/ProgressSwap";
import { ChildrenT } from "@/common/types/ui";
import { isObjOk } from "@/core/lib/dataStructure";
import type { FC } from "react";

type PropsType = {
  propsProgressSwap?: {
    currSwap: number;
    totSwaps: number;
  };
} & ChildrenT;

const AuthPageWrap: FC<PropsType> = ({ propsProgressSwap, children }) => {
  return (
    <div className="w-full grid grid-cols-1 gap-10 mt-[20px]">
      {isObjOk(propsProgressSwap) && (
        <ProgressSwap
          {...({
            maxW: 800,
            ...propsProgressSwap,
          } as PropsType["propsProgressSwap"] & { maxW: number })}
        />
      )}

      <div className="w-full mx-auto max-w-[800px] h-fit rounded-xl border-3 border-neutral-300">
        {children}
      </div>
    </div>
  );
};

export default AuthPageWrap;
