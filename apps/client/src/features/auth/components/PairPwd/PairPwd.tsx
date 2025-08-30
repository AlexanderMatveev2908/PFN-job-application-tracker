/** @jsxImportSource @emotion/react */
"use client";

import { useState, type FC } from "react";
import { pwdFields } from "../../uiFactory/idx";
import FormFieldPwd from "@/common/components/forms/inputs/FormFieldPwd";
import { useFormContext, useWatch } from "react-hook-form";
import { useSyncPortal } from "@/core/hooks/ui/useSyncPortal";
import PwdMatchTracker from "./components/PwdMatchTracker/PwdMatchTracker";
import { SwapModeT } from "@/app/auth/register/page";
import PwdGenerator from "./components/PwdGenerator/PwdGenerator";

type PropsType = {
  isCurrSwap?: boolean;
  swapMode?: SwapModeT;
};

const PairPwd: FC<PropsType> = ({ isCurrSwap = true, swapMode }) => {
  const [isFocus, setIsFocus] = useState(false);

  const formCtx = useFormContext();
  const { control, trigger, getFieldState, formState } = formCtx;
  const pwd = useWatch({
    control,
    name: "password",
  });

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

  const { coords, parentRef } = useSyncPortal([swapMode]);

  const portalConf = {
    showPortal: isCurrSwap && swapMode !== "swapping",
    optDep: [swapMode],
  };

  return (
    <div className="w-full grid grid-cols-1 gap-6">
      <PwdMatchTracker
        {...{
          coords,
          isCurrSwap,
          swapMode,
          isFocus,
          pwd,
          isDirty:
            formState.touchedFields.password ||
            getFieldState("password", formState).isDirty,
        }}
      />

      <FormFieldPwd
        {...{
          el: pwdFields.password,
          control,
          cbChange: () => trigger("confirm_password"),
          cbFocus: () => setIsFocus(true),
          cbBlur: () => setIsFocus(false),
          isPwdShw: isPwdShw,
          handleSvgClick: handlePwdClick,
          optRef: parentRef,
          portalConf,
        }}
      />

      <PwdGenerator {...{ swapMode, isCurrSwap }} />

      <FormFieldPwd
        {...{
          el: pwdFields.confirm_password,
          control,
          cbChange: () => trigger("password"),
          isPwdShw: isConfPwdShw,
          handleSvgClick: handleConfPwd,
          portalConf,
        }}
      />
    </div>
  );
};

export default PairPwd;
