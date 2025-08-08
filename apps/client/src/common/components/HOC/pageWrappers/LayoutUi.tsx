import type { FC, ReactNode } from "react";

type PropsType = {
  children: ReactNode;
};

const LayoutUi: FC<PropsType> = ({ children }) => {
  return (
    <div className="w-full flex flex-col h-full min-h-screen">{children}</div>
  );
};

export default LayoutUi;
