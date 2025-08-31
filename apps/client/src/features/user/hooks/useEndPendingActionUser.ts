import { useDispatch } from "react-redux";
import { useGetUserState } from "./useGetUserState";
import { useEffect, useRef } from "react";
import { userSlice } from "../slices/slice";
import { clearTmr } from "@/core/lib/etc";

export const useEndPendingActionUser = () => {
  const usState = useGetUserState();
  const dispatch = useDispatch();

  const timerID = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (usState.pendingAction)
      timerID.current = setTimeout(() => {
        dispatch(userSlice.actions.endPendingAction());
        clearTmr(timerID);
      }, 1000);

    return () => {
      clearTmr(timerID);
    };
  }, [usState.pendingAction, dispatch]);
};
