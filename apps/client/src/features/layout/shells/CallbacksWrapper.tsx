/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import { useWrapClientListener } from "@/core/hooks/etc/useWrapClientListener";
import { useScroll } from "@/core/hooks/ui/useScroll";
import { getStorage } from "@/core/lib/storage";
import { noticeSlice } from "@/features/notice/slices/slice";
import { useGetUsProfile } from "@/features/user/hooks/useGetUsProfile";
import { userSlice } from "@/features/user/slices/slice";
import { useEffect, type FC } from "react";
import { useDispatch } from "react-redux";

const CallbacksWrapper: FC<ChildrenT> = ({ children }) => {
  useScroll();

  useGetUsProfile();

  const dispatch = useDispatch();
  const { wrapClientListener } = useWrapClientListener();

  useEffect(() => {
    const cb = () => {
      const access_token = (getStorage("access_token") ?? "") as string;
      const notice = getStorage("notice");
      if (access_token) dispatch(userSlice.actions.login({ access_token }));
      if (notice) dispatch(noticeSlice.actions.setNotice(notice));
    };

    wrapClientListener(cb);
  }, [wrapClientListener, dispatch]);

  return children;
};

export default CallbacksWrapper;
