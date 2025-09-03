/** @jsxImportSource @emotion/react */
"use client";

import { useHydration } from "@/core/hooks/etc/hydration/useHydration";
import { useMemo, type FC, type ReactNode } from "react";
import SpinPage from "../../spinners/SpinPage/SpinPage";
import WrapPage from "./WrapPage";
import { ErrApp } from "@/core/lib/err";

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

  const isPending = useMemo(
    () => !isHydrated || isLoading,
    [isHydrated, isLoading]
  );

  if (!isPending && !isApiOk && throwErr)
    throw new ErrApp(
      "Data structure of API response does not fit expected shape ☢️"
    );

  console.log("render");

  return isPending ? (
    <SpinPage />
  ) : isApiOk ? (
    <WrapPage>
      {typeof children === "function" ? children({ isHydrated }) : children}
    </WrapPage>
  ) : null;
};

export default WrapCSR;
