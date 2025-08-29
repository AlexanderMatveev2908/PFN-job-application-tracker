/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import { useScroll } from "@/core/hooks/ui/useScroll";
import { getStorage } from "@/core/lib/storage";
import { genStoreSSR } from "@/core/store";
import { noticeInitState } from "@/features/notice/slices/slice";
import { useRef, type FC } from "react";
import { Provider } from "react-redux";

type PropsType = {
  children: React.ReactNode;
  preloadedState?: any;
};

const Providers: FC<PropsType> = ({ children, preloadedState }) => {
  useScroll();

  const access_token = (getStorage("access_token") ?? "") as string;
  const notice = getStorage("notice");

  const store = useRef(
    genStoreSSR({
      ...preloadedState,
      user: {
        ...preloadedState.user,
        access_token: access_token,
      },
      notice: notice ?? noticeInitState,
    })
  ).current;

  return <Provider store={store}>{children}</Provider>;
};

export default Providers;
