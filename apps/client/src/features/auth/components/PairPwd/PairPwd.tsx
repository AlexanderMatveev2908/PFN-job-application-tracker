/** @jsxImportSource @emotion/react */
"use client";

import { useState, type FC } from "react";
import { pwdFields } from "../../uiFactory/idx";
import FormFieldPwd from "@/common/components/forms/inputs/FormFieldPwd";
import { useFormContext } from "react-hook-form";
import PortalWrapper from "@/common/components/HOC/PortalWrapper";
import { css } from "@emotion/react";
import { useSyncPortal } from "@/core/hooks/ui/useSyncPortal";

const PairPwd: FC = ({}) => {
  const formCtx = useFormContext();
  const { control, trigger } = formCtx;

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
      <PortalWrapper
        {...{
          $CSS: css`
            top: ${coords[0]}px;
            left: ${coords[1]}px;
          `,
          act: "INFO",
        }}
      >
        <div className="w-[75vw] h-[200px] p-5"></div>
      </PortalWrapper>

      <FormFieldPwd
        {...{
          el: pwdFields.password,
          control,
          cbChange: () => trigger("confirm_password"),
          isShw: isPwdShw,
          handleSvgClick: handlePwdClick,
          optRef: parentRef,
        }}
      />

      <FormFieldPwd
        {...{
          el: pwdFields.confirm_password,
          control,
          cbChange: () => trigger("password"),
          isShw: isConfPwdShw,
          handleSvgClick: handleConfPwd,
        }}
      />
    </div>
  );
};

export default PairPwd;
