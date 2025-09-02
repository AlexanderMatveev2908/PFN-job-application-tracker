import { TokenT } from "@/common/types/tokens";
import { extractAadFromCbcHmac } from "@/core/lib/dataStructure";
import { useManageCbcHmac } from "@/core/hooks/etc/tokens/useManageCbcHmac";
import { useUser } from "@/features/user/hooks/useUser";
import { usePathname } from "next/navigation";
import { useEffect } from "react";
import { useWrapAPI } from "../../api/useWrapAPI";
import { cleanupSliceAPI } from "@/features/cleanup/slices/api";

export const useDelCbcHmacByPathAndType = () => {
  const { userState } = useUser();

  const p = usePathname();

  const { delCbcHmac } = useManageCbcHmac();
  const { wrapAPI } = useWrapAPI();
  const [mutate] = cleanupSliceAPI.useCleanCbcHmacMutation();

  useEffect(() => {
    const cb = async () => {
      if (!userState.cbc_hmac_token) return;
      const aad = extractAadFromCbcHmac(userState.cbc_hmac_token);
      if (!aad || p.includes("/verify")) return;

      const { token_t } = aad;
      if (
        (token_t === TokenT.RECOVER_PWD &&
          !p.includes("auth/recover-password")) ||
        (token_t === TokenT.MANAGE_ACC &&
          !["/user/access-manage-account", "/user/manage-account"].some(
            (usPath) => p.includes(usPath)
          ))
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
  }, [userState.cbc_hmac_token, delCbcHmac, p, wrapAPI, mutate]);
};
