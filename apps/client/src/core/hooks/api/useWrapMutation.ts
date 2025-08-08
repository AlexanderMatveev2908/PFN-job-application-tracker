/* eslint-disable @typescript-eslint/no-explicit-any */
import { useDispatch } from "react-redux";
import { useCallback } from "react";
import {
  MutationActionCreatorResult,
  MutationDefinition,
} from "@reduxjs/toolkit/query";
import { useErrAPI } from "./useErrAPI";
import { toastSlice } from "@/features/layout/components/Toast/slices";
import { ErrApiT } from "@/common/types/api";
import { isStr } from "@/core/lib/dataStructure";
import { __cg } from "@/core/lib/log";

export const useWrapMutation = () => {
  const dispatch = useDispatch();

  const { handleErr } = useErrAPI();

  const wrapMutation = useCallback(
    async <T extends MutationDefinition<any, any, any, any>>({
      cbAPI,
      showToast = true,
      hideErr,
    }: {
      cbAPI: () => MutationActionCreatorResult<T>;
      showToast?: boolean;
      hideErr?: boolean;
    }) => {
      try {
        const data = await cbAPI().unwrap();

        __cg("wrapper mutation", data);

        if (showToast)
          dispatch(
            toastSlice.actions.open({
              msg: isStr(data?.msg) ? data.msg! : "Things went good ✅",
              type: "OK",
            })
          );

        return data;
      } catch (err) {
        handleErr({ err: err as ErrApiT<T>, hideErr });
      }
    },
    [handleErr, dispatch]
  );

  return { wrapMutation };
};
