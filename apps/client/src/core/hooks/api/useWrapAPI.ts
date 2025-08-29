import { useCallback } from "react";
import { useDispatch } from "react-redux";
import { useErrAPI } from "./useErrAPI";
import { ResApiT, UnwrappedResApiT } from "@/common/types/api";
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
      cbAPI: () => { unwrap: () => Promise<UnwrappedResApiT<T>> };
      showToast?: boolean;
      hideErr?: boolean;
      throwErr?: boolean;
    }): Promise<UnwrappedResApiT<T>> => {
      try {
        const data = await cbAPI().unwrap();

        __cg("wrapper res api", data);

        if (showToast)
          dispatch(
            toastSlice.actions.open({
              msg: isStr(data?.msg) ? data.msg! : "Things went good ✅",
              type: "OK",
            })
          );

        return data;
      } catch (err) {
        return handleErr({ err: err as ResApiT<T>, hideErr, throwErr });
      }
    },
    [handleErr, dispatch]
  );

  return {
    wrapAPI,
  };
};
