import { TokenT } from "@/common/types/tokens";
import {
  verifySliceAPI,
  VerifyConfEmailReturnT,
  VerifyRecoverPwdReturnT,
} from "../slices/api";
import { useUser } from "@/features/user/hooks/useUser";
import { useRouter } from "next/navigation";
import { useNotice } from "@/features/notice/hooks/useNotice";
import { useCallback, useMemo } from "react";
import { useWrapAPI } from "@/core/hooks/api/useWrapAPI";
import { UnwrappedResT } from "@/common/types/api";
import { useSaveCbcHmac } from "@/features/user/hooks/useSaveCbcHmac";

export type MapperVerifyT = Record<
  TokenT,
  (cbc_hmac_token: string) => Promise<void>
>;

export const useVerify = () => {
  const hookConfEmail = verifySliceAPI.useLazyVerifyConfEmailQuery();
  const hookRecoverPwd = verifySliceAPI.useLazyVerifyRecoverPwdQuery();

  const { loginUser } = useUser();
  const { setNotice } = useNotice();
  const { saveCbcHmac } = useSaveCbcHmac();
  const { wrapAPI } = useWrapAPI();

  const nav = useRouter();

  const wrapHandleErr = useCallback(
    async <T>(cb: () => Promise<UnwrappedResT<T>>) => {
      const res = await cb();

      if (res.isErr) {
        setNotice({
          msg: res?.msg ?? "👻",
          type: "ERR",
        });

        nav.replace("/notice");
        return;
      }

      return res;
    },
    [setNotice, nav]
  );

  const mapperVerify: MapperVerifyT = useMemo(
    () => ({
      CONF_EMAIL: async (cbc_hmac_token: string) => {
        const [triggerRTK] = hookConfEmail;

        const res = await wrapHandleErr(() =>
          wrapAPI<VerifyConfEmailReturnT>({
            cbAPI: () => triggerRTK(cbc_hmac_token),
          })
        );

        if (res?.access_token) {
          loginUser(res.access_token);

          nav.replace("/");
        }
      },
      RECOVER_PWD: async (cbc_hmac_token: string) => {
        const [triggerRTK] = hookRecoverPwd;

        const res = await wrapHandleErr(() =>
          wrapAPI<VerifyRecoverPwdReturnT>({
            cbAPI: () => triggerRTK(cbc_hmac_token),
          })
        );

        if (!res?.isErr) {
          saveCbcHmac(cbc_hmac_token);
          nav.replace("/auth/recover-password");
        }
      },
    }),
    [
      wrapAPI,
      hookConfEmail,
      wrapHandleErr,
      hookRecoverPwd,
      loginUser,
      nav,
      saveCbcHmac,
    ]
  ) as MapperVerifyT;

  return {
    mapperVerify,
  };
};
