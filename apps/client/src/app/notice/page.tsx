/** @jsxImportSource @emotion/react */
"use client";

import WrapCSR from "@/common/components/HOC/pageWrappers/WrapCSR";
import WrapEventPage from "@/common/components/HOC/pageWrappers/WrapEventPage/WrapEventPage";
import LinkShadow from "@/common/components/links/LinkShadow";
import { envApp } from "@/core/constants/env";
import { isStr } from "@/core/lib/dataStructure";
import { getStorage } from "@/core/lib/storage";
import {
  getNoticeState,
  KeyCbT,
  noticeSlice,
  NoticeStateT,
} from "@/features/notice/slices/slice";
import { useUs } from "@/features/user/hooks/useUs";
import { useEffect, type FC } from "react";
import { useDispatch, useSelector } from "react-redux";

const mapCbs: Record<KeyCbT, () => void> = {
  LOGIN: () => console.log("action mapped for key => LOGIN"),
};

const Page: FC = () => {
  const noticeState = useSelector(getNoticeState);
  const usState = useUs();

  const dispatch = useDispatch();

  useEffect(() => {
    const saved = getStorage("notice") as Partial<NoticeStateT>;
    if (saved) dispatch(noticeSlice.actions.setNotice(saved));
  }, [dispatch]);

  useEffect(() => {
    if (isStr(noticeState.keyCb)) mapCbs[noticeState.keyCb]();
  }, [noticeState.keyCb]);

  useEffect(() => {
    if (usState.pendingAction) usState.endPendingAction();
  }, [usState]);

  return (
    <WrapCSR>
      <WrapEventPage
        {...{
          act: noticeState.type,
          msg: noticeState.msg,
        }}
      >
        {noticeState.child === "OPEN_MAIL_APP" && (
          <div className="w-[250px] flex justify-center mt-6">
            <LinkShadow
              {...{
                act: "INFO",
                el: {
                  label: "Open Mail",
                },
                href: `https://mail.google.com/mail/u/0/#search/from%3A${envApp.NEXT_PUBLIC_SMPT_FROM.replace(
                  "@",
                  "%40"
                )}`,
              }}
            />
          </div>
        )}
      </WrapEventPage>
    </WrapCSR>
  );
};

export default Page;
