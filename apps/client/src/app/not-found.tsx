"use client";

import type { FC } from "react";
import WrapEventPage from "@/common/components/HOC/pageWrappers/WrapEventPage/WrapEventPage";
import LinkShadow from "@/common/components/links/LinkShadow";

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
