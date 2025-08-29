/** @jsxImportSource @emotion/react */
"use client";

import WrapCSR from "@/common/components/HOC/pageWrappers/WrapCSR";
import { AadCbcHmacT, CbcHmacTokenT } from "@/common/types/tokens";
import { REG_CBC_HMAC } from "@/core/constants/regex";
import { useWrapClientListener } from "@/core/hooks/etc/useWrapClientListener";
import { hexToDict } from "@/core/lib/dataStructure";
import { useNotice } from "@/features/notice/hooks/useNotice";
import { useVerify } from "@/features/verify/hooks/useVerify";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, type FC } from "react";

const Page: FC = () => {
  const cbcHmacToken = useSearchParams().get("cbc_hmac_token");
  const nav = useRouter();

  const { setNotice } = useNotice();
  const { mapperVerify } = useVerify();
  const { wrapClientListener } = useWrapClientListener();

  useEffect(() => {
    const cb = async () => {
      let aad: AadCbcHmacT | null = null;
      try {
        if (cbcHmacToken && REG_CBC_HMAC.test(cbcHmacToken))
          aad = hexToDict(cbcHmacToken!.split(".")[0]!);
      } catch {
        aad = null;
      }

      if (!aad) {
        setNotice({
          msg: "Invalid Token",
          type: "ERR",
        });
        nav.replace("/notice");
      }

      await mapperVerify[aad!.token_t as CbcHmacTokenT](cbcHmacToken!);
    };

    wrapClientListener(cb);
  }, [cbcHmacToken, setNotice, nav, mapperVerify, wrapClientListener]);

  useEffect(() => {}, []);

  return (
    <WrapCSR
      {...{
        isLoading: true,
      }}
    />
  );
};

export default Page;
