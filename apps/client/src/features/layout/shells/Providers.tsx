/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import { useScroll } from "@/core/hooks/ui/useScroll";
import { getStorage } from "@/core/lib/storage";
import { genStoreSSR } from "@/core/store";
import { useRef, type FC } from "react";
import { Provider } from "react-redux";

type PropsType = {
  children: React.ReactNode;
  preloadedState?: any;
};

const Providers: FC<PropsType> = ({ children, preloadedState }) => {
  useScroll();

  const store = useRef(genStoreSSR(preloadedState)).current;

  const access_token = getStorage("access_token") as string;
  store.getState().user.access_token = access_token ?? "";

  return <Provider store={store}>{children}</Provider>;
};

export default Providers;
