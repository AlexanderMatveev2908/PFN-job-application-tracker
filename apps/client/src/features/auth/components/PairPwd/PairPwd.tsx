/** @jsxImportSource @emotion/react */
"use client";

import { useEffect, useState, type FC } from "react";
import { pwdFields } from "../../uiFactory/idx";
import FormFieldPwd from "@/common/components/forms/inputs/FormFieldPwd";
import { useFormContext, useWatch } from "react-hook-form";
import { useSyncPortal } from "@/core/hooks/ui/useSyncPortal";
import PwdMatchTracker from "./components/PwdMatchTracker/PwdMatchTracker";

type PropsType = {
  isCurrSwap?: boolean;
};

const PairPwd: FC<PropsType> = ({ isCurrSwap = true }) => {
  const formCtx = useFormContext();
  const { control, trigger } = formCtx;
  const pwd = useWatch({
    control,
    name: "password",
  });

  useEffect(() => {
    console.log(pwd);
  }, [pwd]);

  const [isPwdShw, setIsPwdShw] = useState(false);
  const [isConfPwdShw, setIsConfPwdShw] = useState(false);

  const handlePwdClick = () => {
    if (isConfPwdShw) setIsConfPwdShw(false);
    setIsPwdShw(!isPwdShw);
  };

  const handleConfPwd = () => {
    if (isPwdShw) setIsPwdShw(false);
    setIsConfPwdShw(!isConfPwdShw);
  };

  const { coords, parentRef } = useSyncPortal();

  return (
    <div className="w-full grid grid-cols-1 gap-6">
      <PwdMatchTracker
        {...{
          coords,
          isCurrSwap,
        }}
      />

      <FormFieldPwd
        {...{
          el: pwdFields.password,
          control,
          cbChange: () => trigger("confirm_password"),
          isShw: isPwdShw,
          handleSvgClick: handlePwdClick,
          optRef: parentRef,
          portalConf: {
            showPortal: isCurrSwap,
          },
        }}
      />

      <FormFieldPwd
        {...{
          el: pwdFields.confirm_password,
          control,
          cbChange: () => trigger("password"),
          isShw: isConfPwdShw,
          handleSvgClick: handleConfPwd,
          portalConf: {
            showPortal: isCurrSwap,
          },
        }}
      />
    </div>
  );
};

export default PairPwd;
