/** @jsxImportSource @emotion/react */
"use client";

import PairTxtSvg from "@/common/components/elements/PairTxtSvg";
import { linkLogout } from "@/core/uiFactory/links";
import { useState, type FC } from "react";

const LogoutHeader: FC = () => {
  const [isHover, setIsHover] = useState(false);

  return (
    <button
      onMouseEnter={() => setIsHover(true)}
      onMouseLeave={() => setIsHover(false)}
      className="text-neutral-300 hover:text-neutral-950 hover:bg-neutral-300 transition-all duration-300 flex items-center p-2 justify-start gap-6 enabled:hover:cursor-pointer"
    >
      <PairTxtSvg {...{ el: linkLogout, isLoading: false, isHover }} />
    </button>
  );
};

export default LogoutHeader;
