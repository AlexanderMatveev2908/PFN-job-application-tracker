/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { FormManageAccPropsType } from "../types";
import BtnShadow from "@/common/components/buttons/BtnShadow";
import WrapPop from "@/common/components/HOC/WrapPop/WrapPop";
import { usePop } from "@/core/hooks/etc/usePop";
import Portal from "@/common/components/elements/portals/Portal";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { useUser } from "@/features/user/hooks/useUser";
import { userSliceAPI } from "@/features/user/slices/api";
import WrapSwapManageAcc from "./subComponents/WrapSwapManageAcc";

const DelAccountSwap: FC<Omit<FormManageAccPropsType, "swapState">> = ({
  contentRef,
  isCurr,
}) => {
  const { isPop, setIsPop } = usePop();

  const { nav, wrapAPI, setNotice } = useKitHooks();
  const {
    userState: { cbc_hmac_token },
    commonLogoutActions,
  } = useUser();

  const [mutate, { isLoading }] = userSliceAPI.useDeleteAccountMutation();

  const handleDelete = async () => {
    const res = await wrapAPI({
      cbAPI: () => mutate(cbc_hmac_token),
      pushNotice: [401],
    });

    setIsPop(false);

    if (!res) return;

    setNotice({
      msg: "Account Deleted",
      type: "OK",
    });

    commonLogoutActions();

    nav.replace("/notice");
  };

  const testID = "delete_account";

  return (
    <WrapSwapManageAcc
      {...{
        contentRef,
        isCurr,
        title: "Delete Account",
        testID,
      }}
    >
      <Portal
        {...{
          needEvents: true,
        }}
      >
        <WrapPop
          {...{
            isPop,
            setIsPop,
            propsActions: {
              btns: [
                {
                  msg: "Change idea",
                },
                {
                  msg: "Delete",
                  handleClick: handleDelete,
                  isLoading,
                },
              ],
            },
          }}
        >
          <div className="w-full flex justify-center px-8">
            <span className="txt__lg">
              Once confirmed the account will be deleted with all associated
              data without any possibility of recover it.
            </span>
          </div>
        </WrapPop>
      </Portal>

      <div className="w-full flex justify-center px-10">
        <span className="txt__lg">Delete Account and all related data</span>
      </div>

      <div className="mt-[50px] w-[250px] justify-self-center">
        <BtnShadow
          {...{
            el: {
              label: "Delete",
            },
            testID: `${testID}__btn`,
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
