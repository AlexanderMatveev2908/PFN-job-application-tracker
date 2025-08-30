import { useDispatch } from "react-redux";
import { useGetUsState } from "./useGetUsState";
import { useEffect } from "react";
import { userSlice } from "../slices/slice";

export const useEndPendingActionUser = () => {
  const usState = useGetUsState();
  const dispatch = useDispatch();

  useEffect(() => {
    if (usState.pendingAction) dispatch(userSlice.actions.endPendingAction());
  }, [usState, dispatch]);
  return {};
};
