/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { FormManageAccPropsType } from "../types";
import WrapSwapManageAcc from "./subComponents/WrapSwapManageAcc";
import BtnShadow from "@/common/components/buttons/BtnShadow";
import WrapPop from "@/common/components/HOC/WrapPop/WrapPop";
import { usePop } from "@/core/hooks/etc/usePop";
import PortalEvents from "@/common/components/elements/portals/PortalEvents";

const DelAccountSwap: FC<FormManageAccPropsType> = ({ contentRef, isCurr }) => {
  const { isPop, setIsPop } = usePop();

  return (
    <WrapSwapManageAcc
      {...{
        contentRef,
        isCurr,
        title: "Delete Account",
      }}
    >
      <PortalEvents>
        <WrapPop
          {...{
            isPop,
            setIsPop,
          }}
        >
          <div className=""></div>
        </WrapPop>
      </PortalEvents>

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
            handleClick: () => setIsPop(true),
          }}
        />
      </div>
    </WrapSwapManageAcc>
  );
};

export default DelAccountSwap;
