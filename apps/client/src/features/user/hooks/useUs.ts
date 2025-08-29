import { useDispatch } from "react-redux";
import { userSlice } from "../slices/slice";
import { useCallback } from "react";
import { saveStorage } from "@/core/lib/storage";
import { useGetUsState } from "./useGetUsState";

export const useUs = () => {
  const dispatch = useDispatch();

  const loginUser = useCallback(
    (access_token: string) => {
      saveStorage(access_token, { key: "access_token" });
      dispatch(userSlice.actions.login({ access_token }));
    },
    [dispatch]
  );
  const endPendingAction = useCallback(() => {
    dispatch(userSlice.actions.endPendingAction());
  }, [dispatch]);

  return {
    ...useGetUsState(),
    loginUser,
    endPendingAction,
  };
};
