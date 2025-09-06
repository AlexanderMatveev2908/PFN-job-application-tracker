import BaseLayoutPage from "@/common/components/wrappers/pages/BaseLayoutPage";
import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

export const metadata = {
  title: "Access Manage Account 2FA",
};

const Layout: FC<ChildrenT> = ({ children }) => {
  return (
    <BaseLayoutPage
      {...{
        title: "Manage Account 2FA",
      }}
    >
      {children}
    </BaseLayoutPage>
  );
};

export default Layout;
