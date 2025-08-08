/* eslint-disable @typescript-eslint/no-explicit-any */
import { ErrApiT } from "@/common/types/api";
import { isStr } from "@/core/lib/dataStructure";
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
      err: ErrApiT<T>;
      hideErr?: boolean;
      throwErr?: boolean;
    }) => {
      __cg("wrapper error", err);

      const { data } = err;

      if (!hideErr)
        dispatch(
          toastSlice.actions.open({
            msg: isStr(data?.msg) ? data.msg! : "Ops something went wrong ❌",
            type: "ERR",
          })
        );

      if (throwErr) throw err;
    },
    [dispatch]
  );

  return {
    handleErr,
  };
};
