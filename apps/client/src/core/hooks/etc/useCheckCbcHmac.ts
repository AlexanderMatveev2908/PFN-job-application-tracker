import { AadCbcHmacT, TokenT } from "@/common/types/tokens";
import { REG_CBC_HMAC } from "@/core/constants/regex";
import { hexToDict } from "@/core/lib/dataStructure";
import { useNotice } from "@/features/notice/hooks/useNotice";
import { useRouter } from "next/navigation";
import { useCallback } from "react";

export const useCheckCbcHmac = () => {
  const { setNotice } = useNotice();

  const nav = useRouter();

  const checkCbcHmac = useCallback(
    (cbc_hmac_token?: string | null, token_t?: TokenT) => {
      let aad: AadCbcHmacT | null = null;
      try {
        if (cbc_hmac_token && REG_CBC_HMAC.test(cbc_hmac_token))
          aad = hexToDict(cbc_hmac_token!.split(".")[0]!);
      } catch {
        aad = null;
      }

      if (!aad || !Object.values(TokenT).includes(aad.token_t)) {
        setNotice({
          msg: `Invalid Token Format`,
          type: "ERR",
        });
        nav.replace("/notice");

        return;
      }

      if (token_t && aad.token_t !== token_t) {
        setNotice({
          msg: `Invalid Token Type`,
          type: "ERR",
        });
        nav.replace("/notice");

        return;
      }

      return aad;
    },
    [nav, setNotice]
  );

  return {
    checkCbcHmac,
  };
};
