/* eslint-disable @typescript-eslint/no-explicit-any */
import { ResApiT, UnwrappedResApiT } from "@/common/types/api";
import { isStr, serialize } from "@/core/lib/dataStructure";
import { __cg } from "@/core/lib/log";
import { toastSlice } from "@/features/layout/components/Toast/slices";
import { useCallback } from "react";
import { useDispatch } from "react-redux";

export const useErrAPI = () => {
  const dispatch = useDispatch();

  const handleErr = useCallback(
    <T extends Record<string, any>>({
      err,
      hideErr,
      throwErr,
    }: {
      err: ResApiT<T>;
      hideErr?: boolean;
      throwErr?: boolean;
    }): UnwrappedResApiT<T> => {
      __cg("wrapper err api", err);

      const { data } = err;

      if (!hideErr)
        dispatch(
          toastSlice.actions.open({
            msg: isStr(data?.msg) ? data.msg! : "Ops something went wrong ❌",
            type: "ERR",
          })
        );

      if (throwErr) throw err;

      return {
        ...(serialize(err?.data) as any),
        isErr: true,
      };
    },
    [dispatch]
  );

  return {
    handleErr,
  };
};
