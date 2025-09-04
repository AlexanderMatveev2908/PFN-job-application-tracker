/** @jsxImportSource @emotion/react */
"use client";

import LinkShadow from "@/common/components/links/LinkShadow";
import WrapCSR from "@/common/components/pageWrappers/WrapCSR";
import WrapEventPage from "@/common/components/pageWrappers/WrapEventPage/WrapEventPage";
import { envApp } from "@/core/constants/env";
import { isStr } from "@/core/lib/dataStructure";
import { mapperCbs } from "@/features/notice/lib/etc";
import { getNoticeState } from "@/features/notice/slices/slice";
import { useEffect, type FC } from "react";
import { useSelector } from "react-redux";

const Page: FC = () => {
  const noticeState = useSelector(getNoticeState);

  useEffect(() => {
    if (isStr(noticeState.keyCb)) mapperCbs[noticeState.keyCb]();
  }, [noticeState.keyCb]);

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
