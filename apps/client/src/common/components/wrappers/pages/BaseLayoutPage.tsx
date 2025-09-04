import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";
import Title from "../../elements/txt/Title";

type PropsType = {
  title?: string;
} & ChildrenT;

const BaseLayoutPage: FC<PropsType> = ({ title, children }) => {
  return (
    <div className="w-full h-full min-h-screen flex flex-col gap-12">
      {title && (
        <Title
          {...{
            title,
            $twdCls: "3xl",
          }}
        />
      )}

      {children}
    </div>
  );
};

export default BaseLayoutPage;
