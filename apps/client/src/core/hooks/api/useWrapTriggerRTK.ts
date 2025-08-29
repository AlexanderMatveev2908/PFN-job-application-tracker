/* eslint-disable @typescript-eslint/no-explicit-any */
import { useDispatch } from "react-redux";
import { useErrAPI } from "./useErrAPI";
import { useCallback } from "react";
import { ResApiT, UnwrappedResApiT } from "@/common/types/api";
import { toastSlice } from "@/features/layout/components/Toast/slices";
import { isStr } from "@/core/lib/dataStructure";
import { __cg } from "@/core/lib/log";

export const useWrapTriggerRTK = () => {
  const dispatch = useDispatch();
  const { handleErr } = useErrAPI();

  const wrapTrigger = useCallback(
    async <T>({
      cbAPI,
      showToast = true,
      hideErr,
    }: {
      cbAPI: () => { unwrap: () => Promise<UnwrappedResApiT<T>> };
      showToast?: boolean;
      hideErr?: boolean;
    }) => {
      try {
        const data = await cbAPI().unwrap();

        __cg("wrapper trigger RTK", data);

        if (showToast)
          dispatch(
            toastSlice.actions.open({
              msg: isStr(data?.msg) ? data.msg! : "Things went good ✅",
              type: "OK",
            })
          );

        return data;
      } catch (err) {
        handleErr({ err: err as ResApiT<any>, hideErr });
      }
    },

    [dispatch, handleErr]
  );

  return {
    wrapTrigger,
  };
};
