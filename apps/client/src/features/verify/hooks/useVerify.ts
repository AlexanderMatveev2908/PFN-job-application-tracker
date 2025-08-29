import { TokenT } from "@/common/types/tokens";
import { verifySliceAPI, VerifyUserReturnT } from "../slices/sliceAPI";
import { useUs } from "@/features/user/hooks/useUs";
import { useRouter } from "next/navigation";
import { useNotice } from "@/features/notice/hooks/useNotice";
import { useMemo } from "react";
import { useWrapAPI } from "@/core/hooks/api/useWrapAPI";

export type MapperVerifyT = Record<
  TokenT,
  (cbc_hmac_token: string) => Promise<void>
>;

export const useVerify = () => {
  const hookConfEmail = verifySliceAPI.useLazyConfEmailQuery();

  const { loginUser } = useUs();
  const { setNotice } = useNotice();
  const { wrapAPI } = useWrapAPI();

  const nav = useRouter();

  const mapperVerify: MapperVerifyT = useMemo(
    () => ({
      CONF_EMAIL: async (cbc_hmac_token: string) => {
        const [triggerRTK] = hookConfEmail;

        const res = await wrapAPI<VerifyUserReturnT>({
          cbAPI: () => triggerRTK(cbc_hmac_token),
        });

        if (res?.access_token) {
          loginUser(res.access_token);

          nav.replace("/");
        } else {
          setNotice({
            msg: res?.msg ?? "👻",
            type: "ERR",
          });

          nav.replace("/notice");
        }
      },
    }),
    [wrapAPI, hookConfEmail, loginUser, nav, setNotice]
  ) as MapperVerifyT;

  return {
    mapperVerify,
  };
};
