import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";

type PropsType = {
  title: string;
} & ChildrenT;

const BaseLayoutPage: FC<PropsType> = ({ title, children }) => {
  return (
    <div className="w-full h-full min-h-screen flex flex-col gap-12">
      <div className="w-full flex justify-center">
        <span className="txt__3xl grad__txt">{title}</span>
      </div>

      {children}
    </div>
  );
};

export default BaseLayoutPage;
