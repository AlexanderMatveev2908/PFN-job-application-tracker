import { TokenT } from "@/common/types/tokens";
import { extractAadFromCbcHmac } from "@/core/lib/dataStructure";
import { useNotice } from "@/features/notice/hooks/useNotice";
import { useRouter } from "next/navigation";
import { useCallback } from "react";

export const useCheckCbcHmac = () => {
  const { setNotice } = useNotice();

  const nav = useRouter();

  const checkCbcHmac = useCallback(
    (cbc_hmac_token?: string | null, token_t?: TokenT) => {
      const aad = extractAadFromCbcHmac(cbc_hmac_token);

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
