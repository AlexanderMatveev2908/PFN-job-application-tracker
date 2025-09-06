import BaseLayoutPage from "@/common/components/wrappers/pages/BaseLayoutPage";
import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

export const metadata = {
  title: "Create Job Application",
};

const Layout: FC<ChildrenT> = ({ children }) => {
  return (
    <BaseLayoutPage
      {...{
        title: "Create Job Application",
      }}
    >
      {children}
    </BaseLayoutPage>
  );
};

export default Layout;
