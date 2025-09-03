/* eslint-disable @typescript-eslint/no-explicit-any */
import { useCallback } from "react";
import { useErrAPI } from "./useErrAPI";
import { ResApiT } from "@/common/types/api";
import { __cg } from "@/core/lib/log";
import { useMsgAPI } from "./useMsgAPI";

export const useWrapAPI = () => {
  const { handleErr } = useErrAPI();

  const { handleMsgSession } = useMsgAPI();

  const wrapAPI = useCallback(
    async <T>({
      cbAPI,
      showToast = true,
      hideErr,
      throwErr,
      pushNotice,
    }: {
      cbAPI: () => { unwrap: () => Promise<ResApiT<T>> };
      showToast?: boolean;
      hideErr?: boolean;
      throwErr?: boolean;
      pushNotice?: boolean;
    }): Promise<ResApiT<T>["data"] | undefined> => {
      try {
        const data = (await cbAPI().unwrap()) as ResApiT<T>["data"];

        __cg("wrapper res api", data);

        handleMsgSession({ data, showToast });

        return data;
      } catch (err: any) {
        return handleErr({ err: err, hideErr, throwErr, pushNotice });
      }
    },
    [handleErr, handleMsgSession]
  );

  return {
    wrapAPI,
  };
};
