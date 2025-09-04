"use client";

import type { FC } from "react";
import LinkShadow from "@/common/components/links/LinkShadow";
import WrapEventPage from "@/common/components/pageWrappers/WrapEventPage/WrapEventPage";

const NotFound: FC = () => {
  return (
    <WrapEventPage
      {...{
        act: "INFO",
        msg: "The treasure chest is empty. Someone got here before you... 💰",
      }}
    >
      <div className="w-[250px]">
        <LinkShadow
          {...{
            wrapper: "next_link",
            act: "INFO",
            href: "/",
            el: {
              label: "Home",
            },
          }}
        />
      </div>
    </WrapEventPage>
  );
};

export default NotFound;
