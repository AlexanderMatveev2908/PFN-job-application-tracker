import SpinPage from "@/common/components/spinners/SpinPage/SpinPage";
import type { FC } from "react";

const loading: FC = () => {
  return (
    <SpinPage
      {...{
        act: "INFO",
      }}
    />
  );
};

export default loading;
