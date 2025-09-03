/* eslint-disable @typescript-eslint/no-explicit-any */
import { ResApiT } from "@/common/types/api";
import { isStr, serialize } from "@/core/lib/dataStructure";
import { ErrApp } from "@/core/lib/err";
import { __cg } from "@/core/lib/log";
import { apiSlice } from "@/core/store/api";
import { toastSlice } from "@/features/layout/components/Toast/slices";
import { useNotice } from "@/features/notice/hooks/useNotice";
import { useRouter } from "next/navigation";
import { useCallback } from "react";
import { useDispatch } from "react-redux";

export const useErrAPI = () => {
  const dispatch = useDispatch();

  const nav = useRouter();

  const { setNotice } = useNotice();

  const handleErr = useCallback(
    <T>({
      err,
      hideErr,
      throwErr,
      pushNotice,
    }: {
      err: ResApiT<T>["data"];
      hideErr?: boolean;
      throwErr?: boolean;
      pushNotice?: boolean;
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
        if (throwErr && hideErr) throw new ErrApp("Logic Conflict 😡");

        if (!hideErr) {
          const sureMsgExists = isStr(err?.msg)
            ? err.msg!
            : "Ops something went wrong ❌";

          dispatch(
            toastSlice.actions.open({
              msg: sureMsgExists,
              type: "ERR",
            })
          );

          if (err?.status === 429 || pushNotice) {
            setNotice({
              type: "ERR",
              msg: sureMsgExists,
            });

            nav.replace("/notice");

            return;
          }
        }
      }

      if (throwErr) throw err;

      return {
        ...(serialize(err) as any),
        isErr: true,
      };
    },
    [dispatch, nav, setNotice]
  );

  return {
    handleErr,
  };
};
