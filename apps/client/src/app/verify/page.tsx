/** @jsxImportSource @emotion/react */
"use client";

import WrapCSR from "@/common/components/HOC/pageWrappers/WrapCSR";
import { REG_CBC_HMAC } from "@/core/constants/regex";
import { hexToDict } from "@/core/lib/dataStructure";
import { useNotice } from "@/features/notice/hooks/useNotice";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, type FC } from "react";

const Page: FC = () => {
  const cbcHmacToken = useSearchParams().get("cbc_hmac_token");

  const { setNotice } = useNotice();

  const nav = useRouter();

  useEffect(() => {
    if (!cbcHmacToken || !REG_CBC_HMAC.test(cbcHmacToken)) {
      setNotice({
        msg: "Invalid Token",
        type: "ERR",
      });
      nav.replace("/notice");
    }
  }, [cbcHmacToken, setNotice, nav]);

  const hexStr = cbcHmacToken?.split(".")[0];

  console.log(hexToDict(hexStr!));

  return (
    <WrapCSR
      {...{
        isLoading: true,
      }}
    />
  );
};

export default Page;
