/* eslint-disable @typescript-eslint/no-explicit-any */
import { useCallback } from "react";
import { useDispatch } from "react-redux";
import { useErrAPI } from "./useErrAPI";
import { ResApiT } from "@/common/types/api";
import { toastSlice } from "@/features/layout/components/Toast/slices";
import { __cg } from "@/core/lib/log";
import { isStr } from "@/core/lib/dataStructure";

export const useWrapAPI = () => {
  const dispatch = useDispatch();
  const { handleErr } = useErrAPI();

  const wrapAPI = useCallback(
    async <T>({
      cbAPI,
      showToast = true,
      hideErr,
      throwErr,
    }: {
      cbAPI: () => { unwrap: () => Promise<ResApiT<T>> };
      showToast?: boolean;
      hideErr?: boolean;
      throwErr?: boolean;
    }): Promise<ResApiT<T>["data"]> => {
      try {
        const data = (await cbAPI().unwrap()) as ResApiT<T>["data"];

        __cg("wrapper res api", data);

        if (showToast)
          dispatch(
            toastSlice.actions.open({
              msg: isStr(data?.msg) ? data.msg! : "Things went good ✅",
              type: "OK",
            })
          );

        return data;
      } catch (err: any) {
        return handleErr({ err: err, hideErr, throwErr });
      }
    },
    [handleErr, dispatch]
  );

  return {
    wrapAPI,
  };
};
