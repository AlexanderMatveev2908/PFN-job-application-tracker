/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { FormManageAccPropsType } from "../types";
import WrapSwapManageAcc from "./subComponents/WrapSwapManageAcc";
import BtnShadow from "@/common/components/buttons/BtnShadow";

const DelAccountSwap: FC<FormManageAccPropsType> = ({ contentRef, isCurr }) => {
  return (
    <WrapSwapManageAcc
      {...{
        contentRef,
        isCurr,
        title: "Delete Account",
      }}
    >
      <div className="w-full flex justify-center px-10">
        <span className="txt__md">
          Once confirmed the account will be deleted with all associated data
          without any possibility of recover it.
        </span>
      </div>

      <div className="mt-[50px] w-[250px] justify-self-center">
        <BtnShadow
          {...{
            el: {
              label: "Delete",
            },
            testID: "delete_account__btn",
            isLoading: false,
            act: "ERR",
            handleClick: () => console.log("clicked"),
          }}
        />
      </div>
    </WrapSwapManageAcc>
  );
};

export default DelAccountSwap;
