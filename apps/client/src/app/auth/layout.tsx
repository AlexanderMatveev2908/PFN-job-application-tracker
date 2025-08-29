"use client";

import BaseLayoutPage from "@/common/components/HOC/pageWrappers/BaseLayoutPage";
import { ChildrenT } from "@/common/types/ui";
import { captAll } from "@/core/lib/formatters";
import { useGetUsState } from "@/features/user/hooks/useGetUsState";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, type FC } from "react";

const Layout: FC<ChildrenT> = ({ children }) => {
  const p = usePathname();
  const last = p.split("/").pop();

  const nav = useRouter();
  const usState = useGetUsState();

  useEffect(() => {
    if (usState.isLogged && !usState.pendingAction) nav.replace("/");
  }, [usState.isLogged, usState.pendingAction, nav]);

  return (
    <BaseLayoutPage
      {...{
        title: captAll(last?.replace("-", " ")),
      }}
    >
      {children}
    </BaseLayoutPage>
  );
};

export default Layout;
