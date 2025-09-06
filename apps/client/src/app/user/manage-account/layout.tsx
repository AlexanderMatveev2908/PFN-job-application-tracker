import BaseLayoutPage from "@/common/components/wrappers/pages/BaseLayoutPage";
import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

export const metadata = {
  title: "Manage Account",
};

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
