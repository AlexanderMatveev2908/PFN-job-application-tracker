/* eslint-disable @typescript-eslint/no-explicit-any */
import { Dispatch, UnknownAction } from "@reduxjs/toolkit";
import { REG_JWT } from "@/core/constants/regex";
import { userSlice } from "@/features/user/slices/slice";
import { __cg } from "@/core/lib/log";
import { StoreStateT } from "../..";

export const handleErrorsActions =
  (store: any) => (next: Dispatch<any>) => (action: UnknownAction) => {
    const { payload: { data } = {} } = (action ?? {}) as any;

    try {
      const pendingAction = store.getState().user.pendingAction;
      if (pendingAction || (!data?.refreshFailed && !data?.refreshed))
        return next(action);

      const isLogged = REG_JWT.test(
        (store.getState() as StoreStateT).user.access_token ?? ""
      );

      if (data?.refreshed && !isLogged) {
        store.dispatch(
          userSlice.actions.login({ access_token: data.access_token })
        );
        window.location.replace("/");
      }

      if (data?.refreshFailed && isLogged) {
        store.dispatch(userSlice.actions.logout());
        window.location.replace("/");
      }
    } catch (err: any) {
      __cg("err mdw", err);

      return next(action);
    }

    return next(action);
  };
