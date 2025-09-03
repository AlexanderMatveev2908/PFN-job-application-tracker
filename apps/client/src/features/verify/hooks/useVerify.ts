import { TokenT } from "@/common/types/tokens";
import { verifySliceAPI, VerifyCbcHmacArgT } from "../slices/api";
import { useUser } from "@/features/user/hooks/useUser";
import { useRouter } from "next/navigation";
import { useCallback, useMemo } from "react";
import { useWrapAPI } from "@/core/hooks/api/useWrapAPI";
import { TagAPI } from "@/common/types/api";
import { useManageCbcHmac } from "@/core/hooks/etc/tokens/useManageCbcHmac";
import { useDispatch } from "react-redux";
import { apiSlice } from "@/core/store/api";

export type MapperVerifyT = Record<
  TokenT,
  (cbc_hmac_token: string) => Promise<void>
>;

export const useVerify = () => {
  const [triggerRTK] = verifySliceAPI.useLazyVerifyCbcHmacQuery();

  const { loginUser } = useUser();
  const { saveCbcHmac } = useManageCbcHmac();
  const { wrapAPI } = useWrapAPI();
  const dispatch = useDispatch();

  const nav = useRouter();

  const wrapMainCb = useCallback(
    async (data: VerifyCbcHmacArgT) => {
      const res = await wrapAPI({
        cbAPI: () => triggerRTK(data),
        pushNotice: true,
      });

      return res;
    },
    [, triggerRTK, wrapAPI]
  );

  const loginCb = useCallback(
    (access_token: string) => {
      loginUser(access_token);
      dispatch(apiSlice.util.invalidateTags([TagAPI.USER]));
      nav.replace("/");
    },
    [dispatch, nav, loginUser]
  );

  const mapperVerify: MapperVerifyT = useMemo(
    () => ({
      CONF_EMAIL: async (cbc_hmac_token: string) => {
        const res = await wrapMainCb({
          cbc_hmac_token,
          endpoint: "confirm-email",
        });

        if (!res) return;

        if (res?.access_token) {
          loginCb(res.access_token);
        }
      },
      RECOVER_PWD: async (cbc_hmac_token: string) => {
        const res = await wrapMainCb({
          cbc_hmac_token,
          endpoint: "recover-pwd",
        });

        if (!res) return;

        saveCbcHmac(cbc_hmac_token);
        nav.replace("/auth/recover-password");
      },

      CHANGE_EMAIL: async (cbc_hmac_token: string) => {
        const res = await wrapMainCb({
          cbc_hmac_token,
          endpoint: "new-email",
        });

        if (!res) return;

        if (res?.access_token) {
          loginCb(res.access_token);
        }
      },
    }),
    [wrapMainCb, loginCb, nav, saveCbcHmac]
  ) as MapperVerifyT;

  return {
    mapperVerify,
  };
};
