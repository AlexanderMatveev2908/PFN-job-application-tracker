/** @jsxImportSource @emotion/react */
"use client";

import PairTxtSvg from "@/common/components/elements/PairTxtSvg";
import { linkLogout } from "@/core/uiFactory/links";
import { useUser } from "@/features/user/hooks/useUser";
import type { FC } from "react";

type PropsType = {
  handleClick: () => void;
};

const SideLogout: FC<PropsType> = ({ handleClick }) => {
  const { isLoggingOut, logoutUser } = useUser();

  return (
    <button
      onClick={async () => {
        await logoutUser();
        handleClick();
      }}
      className="link__app flex items-center justify-start gap-6"
    >
      <PairTxtSvg {...{ el: linkLogout, isLoading: isLoggingOut }} />
    </button>
  );
};

export default SideLogout;
