/** @jsxImportSource @emotion/react */
"use client";

import WrapCSR from "@/common/components/HOC/pageWrappers/WrapCSR";
import { useCheckCbcHmac } from "@/core/hooks/etc/useCheckCbcHmac";
import { useRunOnHydrate } from "@/core/hooks/etc/useRunOnHydrate";
import { useVerify } from "@/features/verify/hooks/useVerify";
import { useSearchParams } from "next/navigation";
import { useCallback, type FC } from "react";

const Page: FC = () => {
  const cbcHmacToken = useSearchParams().get("cbc_hmac_token");

  const { mapperVerify } = useVerify();

  const { checkCbcHmac } = useCheckCbcHmac();

  const cb = useCallback(async () => {
    const aad = checkCbcHmac(cbcHmacToken);

    if (aad) await mapperVerify[aad.token_t](cbcHmacToken!);
  }, [cbcHmacToken, checkCbcHmac, mapperVerify]);

  useRunOnHydrate({ cb });

  return (
    <WrapCSR
      {...{
        isLoading: true,
      }}
    />
  );
};

export default Page;
