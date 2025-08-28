import { useDispatch, useSelector } from "react-redux";
import { getUserState, userSlice } from "../slices/slice";
import { useCallback } from "react";
import { saveStorage } from "@/core/lib/storage";

export const useUs = () => {
  const userState = useSelector(getUserState);

  const disp = useDispatch();

  const loginUser = useCallback(
    (access_token: string) => {
      saveStorage(access_token, { key: "access_token" });
      disp(userSlice.actions.login({ access_token }));
    },
    [disp]
  );

  return {
    disp,
    userState,
    loginUser,
  };
};
