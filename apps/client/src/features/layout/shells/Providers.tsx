/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import { genStoreSSR } from "@/core/store";
import { useRef, type FC } from "react";
import { Provider } from "react-redux";

type PropsType = {
  children: React.ReactNode;
  preloadedState?: any;
};

const Providers: FC<PropsType> = ({ children, preloadedState }) => {
  const store = useRef(
    genStoreSSR({
      ...preloadedState,
    })
  ).current;

  return <Provider store={store}>{children}</Provider>;
};

export default Providers;
