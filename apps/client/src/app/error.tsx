/* eslint-disable @typescript-eslint/no-explicit-any */
/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { CircleAlert } from "lucide-react";
import WrapEventPage from "@/common/components/HOC/pageWrappers/WrapEventPage";
import WrapShadow from "@/common/components/HOC/buttonWrappers/WrapShadow";
import { __cg } from "@/core/lib/log";

type PropsType = {
  error: any;
  reset: () => void;
};

const Err: FC<PropsType> = ({ error: err }: PropsType) => {
  __cg("err", err);

  return (
    <WrapEventPage
      {...{
        act: "ERR",
        msg: err?.msg ?? err?.data?.msg ?? err?.message ?? "Unmown error...❌",
        Svg: CircleAlert,
      }}
    >
      <div className="w-[250px]">
        <WrapShadow
          {...{
            wrapper: "html_button",
            act: "ERR",
            el: { label: "Refresh" },
            handleClick: () => location.reload(),
          }}
        />
      </div>
    </WrapEventPage>
  );
};

export default Err;
