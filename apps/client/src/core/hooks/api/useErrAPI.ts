/* eslint-disable @typescript-eslint/no-explicit-any */
import { ResApiT } from "@/common/types/api";
import { isStr, serialize } from "@/core/lib/dataStructure";
import { __cg } from "@/core/lib/log";
import { apiSlice } from "@/core/store/api";
import { toastSlice } from "@/features/layout/components/Toast/slices";
import { useRouter } from "next/navigation";
import { useCallback } from "react";
import { useDispatch } from "react-redux";

export const useErrAPI = () => {
  const dispatch = useDispatch();

  const nav = useRouter();

  const handleErr = useCallback(
    <T>({
      err,
      hideErr,
      throwErr,
    }: {
      err: ResApiT<T>["data"];
      hideErr?: boolean;
      throwErr?: boolean;
    }): ResApiT<T>["data"] | undefined => {
      __cg("wrapper err api", err);

      if (err?.refreshFailed) {
        dispatch(
          toastSlice.actions.open({
            msg: "session expired",
            type: "ERR",
          })
        );

        dispatch(apiSlice.util.resetApiState());
        nav.replace("/auth/login");

        return;
      } else {
        if (!hideErr)
          dispatch(
            toastSlice.actions.open({
              msg: isStr(err?.msg) ? err.msg! : "Ops something went wrong ❌",
              type: "ERR",
            })
          );
      }

      if (throwErr) throw err;

      return {
        ...(serialize(err) as any),
        isErr: true,
      };
    },
    [dispatch, nav]
  );

  return {
    handleErr,
  };
};
