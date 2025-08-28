/** @jsxImportSource @emotion/react */
"use client";

import WrapEventPage from "@/common/components/HOC/pageWrappers/WrapEventPage/WrapEventPage";
import { getNoticeState } from "@/features/notice/slices/slice";
import type { FC } from "react";
import { useSelector } from "react-redux";

const Page: FC = () => {
  const noticeState = useSelector(getNoticeState);

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
