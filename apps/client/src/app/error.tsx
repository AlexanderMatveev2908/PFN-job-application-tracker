/* eslint-disable @typescript-eslint/no-explicit-any */
/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { __cg } from "@/core/lib/log";
import BtnShadow from "@/common/components/buttons/BtnShadow";
import WrapEventPage from "@/common/components/pageWrappers/WrapEventPage/WrapEventPage";

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
      }}
    >
      <div className="w-[250px]">
        <BtnShadow
          {...{
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
