import BaseLayoutPage from "@/common/components/HOC/pageWrappers/BaseLayoutPage";
import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

const Layout: FC<ChildrenT> = ({ children }) => {
  return (
    <BaseLayoutPage
      {...{
        title: "Register",
      }}
    >
      {children}
    </BaseLayoutPage>
  );
};

export default Layout;
