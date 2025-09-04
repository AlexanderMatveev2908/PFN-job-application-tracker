import BaseLayoutPage from "@/common/components/pageWrappers/BaseLayoutPage";
import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

const Layout: FC<ChildrenT> = ({ children }) => {
  return (
    <BaseLayoutPage
      {...{
        title: "Manage Account",
      }}
    >
      {children}
    </BaseLayoutPage>
  );
};

export default Layout;
