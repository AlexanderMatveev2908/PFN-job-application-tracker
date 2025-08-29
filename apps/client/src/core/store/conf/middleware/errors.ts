/* eslint-disable @typescript-eslint/no-explicit-any */
import { __cg } from "@/core/lib/log";
import { Dispatch, UnknownAction } from "@reduxjs/toolkit";

export const handleErrorsActions =
  (store: any) => (next: Dispatch<any>) => (action: UnknownAction) => {
    const { payload: { data } = {} } = (action ?? {}) as any;

    if (!data?.refreshFailed) return action;

    __cg("mdw", data);

    return next(action);
  };
