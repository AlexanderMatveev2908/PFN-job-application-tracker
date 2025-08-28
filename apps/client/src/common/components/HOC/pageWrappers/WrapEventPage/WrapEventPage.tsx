/** @jsxImportSource @emotion/react */
"use client";

import { AppEventT } from "@/common/types/api";
import type { FC } from "react";
import { $argClr } from "@/core/uiFactory/style";
import BounceIconSSR from "../../../elements/BounceIconSSR/BounceIconSSR";
import { ChildrenT } from "@/common/types/ui";
import { SvgsAppEvents } from "./uiFactory";

type PropsType = {
  act: AppEventT;
  msg: string;
} & ChildrenT;

const WrapEventPage: FC<PropsType> = ({ act, msg, children }) => {
  const $clr = $argClr[act];

  return (
    <div className="w-full flex flex-col items-center justify-center gap-10 sm:gap-16">
      <BounceIconSSR
        {...{
          act,
          Svg: SvgsAppEvents[act],
        }}
      />

      <div className="w-full flex justify-center max-w-[90%] sm:max-w-[75%]">
        <span
          className="txt__lg"
          style={{
            color: $clr,
          }}
        >
          {msg}
        </span>
      </div>

      {children}
    </div>
  );
};

export default WrapEventPage;
