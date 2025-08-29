/* eslint-disable @typescript-eslint/no-explicit-any */
import { __cg } from "@/core/lib/log";
import { Dispatch, UnknownAction } from "@reduxjs/toolkit";

export const handleErrorsActions =
  (store: any) => (next: Dispatch<any>) => (action: UnknownAction) => {
    const { payload, type } = action;

    __cg("mdw", payload, type);

    return next(action);
  };
