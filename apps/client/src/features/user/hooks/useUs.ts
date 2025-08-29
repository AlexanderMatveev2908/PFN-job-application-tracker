import { useDispatch } from "react-redux";
import { userSlice } from "../slices/slice";
import { useCallback } from "react";
import { saveStorage } from "@/core/lib/storage";
import { useGetUsState } from "./useGetUsState";

export const useUs = () => {
  const disp = useDispatch();

  const loginUser = useCallback(
    (access_token: string) => {
      saveStorage(access_token, { key: "access_token" });
      disp(userSlice.actions.login({ access_token }));
    },
    [disp]
  );
  const endPendingAction = useCallback(() => {
    disp(userSlice.actions.endPendingAction());
  }, [disp]);

  return {
    ...useGetUsState(),
    loginUser,
    endPendingAction,
  };
};
