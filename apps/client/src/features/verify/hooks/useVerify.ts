import { TokenT } from "@/common/types/tokens";
import { verifySliceAPI } from "../slices/sliceAPI";
import { useUs } from "@/features/user/hooks/useUs";
import { useRouter } from "next/navigation";
import { useNotice } from "@/features/notice/hooks/useNotice";
import { useDispatch } from "react-redux";
import { toastSlice } from "@/features/layout/components/Toast/slices";
import { useMemo } from "react";
import { __cg } from "@/core/lib/log";
import { ResApiT } from "@/common/types/api";

export type MapperVerifyT = Record<
  TokenT,
  (cbc_hmac_token: string) => Promise<void>
>;

export const useVerify = () => {
  const hookConfEmail = verifySliceAPI.useLazyConfEmailQuery();

  const { loginUser } = useUs();
  const { setNotice } = useNotice();

  const disp = useDispatch();
  const nav = useRouter();

  const mapperVerify: MapperVerifyT = useMemo(
    () => ({
      CONF_EMAIL: async (cbc_hmac_token: string) => {
        const [triggerRTK, res] = hookConfEmail;

        const { data, isSuccess, error } = await triggerRTK(cbc_hmac_token);

        __cg(data, res);

        disp(
          toastSlice.actions.open({
            msg:
              (isSuccess ? data?.msg : (error as ResApiT<void>)?.data?.msg) ??
              "👻",
            type: isSuccess ? "OK" : "ERR",
          })
        );

        if (data?.access_token) {
          disp(
            toastSlice.actions.open({
              msg: data?.msg ?? "👻",
              type: "OK",
            })
          );

          loginUser(data.access_token);

          nav.replace("/");
        } else {
          setNotice({
            msg: data?.msg,
            type: "ERR",
          });

          nav.replace("/notice");
        }
      },
    }),
    [disp, hookConfEmail, loginUser, nav, setNotice]
  ) as MapperVerifyT;

  return {
    mapperVerify,
  };
};
