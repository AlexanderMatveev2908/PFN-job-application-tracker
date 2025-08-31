/** @jsxImportSource @emotion/react */
"use client";

import PairTxtSvg from "@/common/components/elements/PairTxtSvg";
import { linkLogout } from "@/core/uiFactory/links";
import { useUser } from "@/features/user/hooks/useUser";
import { useState, type FC } from "react";

const LogoutHeader: FC = () => {
  const [isHover, setIsHover] = useState(false);

  const { logoutUser, isLoadingLoggingOut } = useUser();

  return (
    <button
      onClick={logoutUser}
      onMouseEnter={() => setIsHover(true)}
      onMouseLeave={() => setIsHover(false)}
      className="text-neutral-300 hover:text-neutral-950 hover:bg-neutral-300 transition-all duration-300 flex items-center p-2 justify-start gap-6 enabled:hover:cursor-pointer"
    >
      <PairTxtSvg
        {...{ el: linkLogout, isLoading: isLoadingLoggingOut, isHover }}
      />
    </button>
  );
};

export default LogoutHeader;
