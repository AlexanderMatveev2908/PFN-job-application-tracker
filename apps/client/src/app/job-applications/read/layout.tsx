import BaseLayoutPage from "@/common/components/wrappers/pages/BaseLayoutPage";
import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

export const metadata = {
  title: "Job Applications",
};

const Layout: FC<ChildrenT> = ({ children }) => {
  return (
    <BaseLayoutPage
      {...{
        title: "Job Applications",
      }}
    >
      {children}
    </BaseLayoutPage>
  );
};

export default Layout;
