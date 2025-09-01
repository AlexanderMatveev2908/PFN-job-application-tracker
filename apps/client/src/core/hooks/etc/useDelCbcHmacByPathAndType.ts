import { TokenT } from "@/common/types/tokens";
import { extractAadFromCbcHmac } from "@/core/lib/dataStructure";
import { useManageCbcHmac } from "@/features/user/hooks/useManageCbcHmac";
import { useUser } from "@/features/user/hooks/useUser";
import { usePathname } from "next/navigation";
import { useEffect } from "react";

export const useDelCbcHmacByPathAndType = () => {
  const { userState } = useUser();

  const p = usePathname();

  const { delCbcHmac } = useManageCbcHmac();

  useEffect(() => {
    if (!userState.cbc_hmac_token) return;
    const aad = extractAadFromCbcHmac(userState.cbc_hmac_token);
    if (!aad) return;

    if (
      aad.token_t === TokenT.RECOVER_PWD &&
      !p.includes("auth/recover-password")
    )
      delCbcHmac();
  }, [userState.cbc_hmac_token, delCbcHmac, p]);
};
