/** @jsxImportSource @emotion/react */
"use client";

import { useHydration } from "@/core/hooks/etc/hydration/useHydration";
import type { FC, ReactNode } from "react";
import SpinPage from "../../spinners/SpinPage/SpinPage";
import WrapPage from "./WrapPage";

type PropsType = {
  isLoading?: boolean;
  isApiOk?: boolean;
  throwErr?: boolean;
  children?:
    | ReactNode
    | (({ isHydrated }: { isHydrated: boolean }) => ReactNode);
};

const WrapCSR: FC<PropsType> = ({
  isApiOk = true,
  isLoading,
  throwErr,
  children,
}) => {
  const { isHydrated } = useHydration();

  const isPending = !isHydrated || isLoading;

  if (!isPending && !isApiOk && throwErr)
    throw {
      msg: "Data structure of API response does not fit expected shape ☢️",
    };

  return isPending ? (
    <SpinPage />
  ) : isApiOk ? (
    <WrapPage>
      {typeof children === "function" ? children({ isHydrated }) : children}
    </WrapPage>
  ) : null;
};

export default WrapCSR;
