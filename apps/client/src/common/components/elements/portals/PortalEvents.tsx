/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import { useHydration } from "@/core/hooks/etc/hydration/useHydration";
import type { FC } from "react";
import { createPortal } from "react-dom";

type PropsType = {} & ChildrenT;

const PortalEvents: FC<PropsType> = ({ children }) => {
  const { isHydrated } = useHydration();
  if (!isHydrated) return null;

  return createPortal(children, document.body);
};

export default PortalEvents;
