"use client";

import BaseLayoutPage from "@/common/components/HOC/pageWrappers/BaseLayoutPage";
import { ChildrenT } from "@/common/types/ui";
import { captAll } from "@/core/lib/formatters";
import { usePathname } from "next/navigation";
import type { FC } from "react";

const Layout: FC<ChildrenT> = ({ children }) => {
  const p = usePathname();
  const last = p.split("/").pop();

  return (
    <BaseLayoutPage
      {...{
        title: captAll(last),
      }}
    >
      {children}
    </BaseLayoutPage>
  );
};

export default Layout;
