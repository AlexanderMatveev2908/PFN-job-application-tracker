/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import { REG_JWT } from "@/core/constants/regex";
import { useWrapClientListener } from "@/core/hooks/etc/useWrapClientListener";
import { useScroll } from "@/core/hooks/ui/useScroll";
import { isObjOk } from "@/core/lib/dataStructure";
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

      if (REG_JWT.test(access_token))
        dispatch(userSlice.actions.setAccessToken({ access_token }));
      if (isObjOk(notice)) dispatch(noticeSlice.actions.setNotice(notice!));
    };

    wrapClientListener(cb);
  }, [wrapClientListener, dispatch]);

  return children;
};

export default CallbacksWrapper;
