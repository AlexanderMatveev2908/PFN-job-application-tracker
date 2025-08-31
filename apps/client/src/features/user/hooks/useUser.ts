import { useDispatch } from "react-redux";
import { userSlice } from "../slices/slice";
import { useCallback } from "react";
import { saveStorage } from "@/core/lib/storage";
import { useGetUserState } from "./useGetUserState";

export const useUser = () => {
  const dispatch = useDispatch();

  const loginUser = useCallback(
    (access_token: string) => {
      saveStorage(access_token, { key: "access_token" });
      dispatch(userSlice.actions.login({ access_token }));
    },
    [dispatch]
  );

  return {
    userState: useGetUserState(),
    loginUser,
  };
};
