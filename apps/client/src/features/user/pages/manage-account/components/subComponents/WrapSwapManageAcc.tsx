/** @jsxImportSource @emotion/react */
"use client";

import Title from "@/common/components/elements/txt/Title";
import WrapSwap, {
  PropsTypeWrapSwap,
} from "@/common/components/swap/subComponents/WrapSwap";
import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

type PropsType = {
  title: string;
} & ChildrenT &
  Omit<PropsTypeWrapSwap, "children">;

const WrapSwapManageAcc: FC<PropsType> = ({
  children,
  contentRef,
  isCurr,
  title,
}) => {
  return (
    <WrapSwap
      {...{
        contentRef,
        isCurr,
      }}
    >
      <div className="cont__grid__lg py-5">
        <Title
          {...{
            title,
            $twdCls: "2xl",
          }}
        />
        {children}
      </div>
    </WrapSwap>
  );
};

export default WrapSwapManageAcc;
