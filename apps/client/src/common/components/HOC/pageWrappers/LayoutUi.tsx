import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

const LayoutUi: FC<ChildrenT> = ({ children }) => {
  return (
    <div className="w-full flex flex-col h-full min-h-screen">{children}</div>
  );
};

export default LayoutUi;
