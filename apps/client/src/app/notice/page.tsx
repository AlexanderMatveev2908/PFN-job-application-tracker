/** @jsxImportSource @emotion/react */
"use client";

import WrapEventPage from "@/common/components/HOC/pageWrappers/WrapEventPage/WrapEventPage";
import { getStorage } from "@/core/lib/storage";
import {
  getNoticeState,
  noticeSlice,
  NoticeStateT,
} from "@/features/notice/slices/slice";
import { useEffect, type FC } from "react";
import { useDispatch, useSelector } from "react-redux";

const Page: FC = () => {
  const noticeState = useSelector(getNoticeState);

  const dispatch = useDispatch();
  useEffect(() => {
    const saved = getStorage("NOTICE") as Partial<NoticeStateT>;
    if (saved) dispatch(noticeSlice.actions.setNotice(saved));
  }, [dispatch]);

  return (
    <div className="w-full">
      <WrapEventPage
        {...{
          act: noticeState.type,
          msg: noticeState.msg,
        }}
      >
        <div className=""></div>
      </WrapEventPage>
    </div>
  );
};

export default Page;
