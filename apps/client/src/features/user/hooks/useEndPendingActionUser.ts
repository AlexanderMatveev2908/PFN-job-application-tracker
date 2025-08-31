import { useDispatch } from "react-redux";
import { useGetUserState } from "./useGetUserState";
import { useEffect } from "react";
import { userSlice } from "../slices/slice";

export const useEndPendingActionUser = () => {
  const usState = useGetUserState();
  const dispatch = useDispatch();

  useEffect(() => {
    if (usState.pendingAction) dispatch(userSlice.actions.endPendingAction());
  }, [usState.pendingAction, dispatch]);
};
