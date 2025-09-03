/** @jsxImportSource @emotion/react */
"use client";

import { UserT } from "@/features/user/types";
import { CircleAlert, CircleCheckBig } from "lucide-react";
import type { FC } from "react";

type PropsType = {
  user: UserT | null;
};

const NoticeSetup2FA: FC<PropsType> = ({ user }) => {
  const Svg = user?.use_2FA ? CircleCheckBig : CircleAlert;
  const $baseTwd = "w-[150px] h-[150px]";

  const msg = user?.use_2FA
    ? "User has 2Fa setup"
    : "User need to confirm account before setup 2FA";

  return (
    <div className="cont__grid__lg justify-items-center">
      <Svg
        className={`${$baseTwd} ${
          user?.use_2FA ? "text-green-600" : "text-red-600"
        }`}
      />

      <span className="w-[80%] txt__lg text-center">{msg}</span>
    </div>
  );
};

export default NoticeSetup2FA;
