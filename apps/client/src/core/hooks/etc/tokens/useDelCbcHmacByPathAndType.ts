import { TokenT } from "@/common/types/tokens";
import { extractAadFromCbcHmac } from "@/core/lib/dataStructure";
import { useUser } from "@/features/user/hooks/useUser";
import { usePathname } from "next/navigation";
import { useEffect } from "react";
import { useWrapAPI } from "../../api/useWrapAPI";
import { cleanupSliceAPI } from "@/features/cleanup/slices/api";

export const useDelCbcHmacByPathAndType = () => {
  const { userState, delCbcHmac } = useUser();

  const p = usePathname();

  const { wrapAPI } = useWrapAPI();
  const [mutate] = cleanupSliceAPI.useCleanCbcHmacMutation();

  useEffect(() => {
    const cb = async () => {
      if (!userState.cbc_hmac_token || userState.pendingActionCbcHmac) return;
      const aad = extractAadFromCbcHmac(userState.cbc_hmac_token);
      if (!aad) return;

      const { token_t } = aad;
      if (
        (token_t === TokenT.RECOVER_PWD &&
          !p.includes("auth/recover-password")) ||
        (token_t === TokenT.MANAGE_ACC &&
          !["/user/manage-account", "/user/access-manage-account-2FA"].some(
            (allowed) => p.includes(allowed)
          )) ||
        (token_t === TokenT.LOGIN_2FA && !p.includes("/auth/login-2FA")) ||
        (token_t === TokenT.MANAGE_ACC_2FA &&
          !p.includes("/user/access-manage-account-2FA"))
      ) {
        delCbcHmac();

        await wrapAPI({
          cbAPI: () => mutate(userState.cbc_hmac_token),
          showToast: false,
          hideErr: true,
        });
      }
    };

    cb();
  }, [
    userState.cbc_hmac_token,
    delCbcHmac,
    p,
    wrapAPI,
    mutate,
    userState.pendingActionCbcHmac,
  ]);
};
