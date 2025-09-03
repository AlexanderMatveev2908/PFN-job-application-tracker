import { useDispatch } from "react-redux";
import { userSlice } from "../slices/slice";
import { useCallback } from "react";
import { clearStorage, saveStorage } from "@/core/lib/storage";
import { useGetUserState } from "./useGetUserState";
import { useWrapAPI } from "@/core/hooks/api/useWrapAPI";
import { authSliceAPI } from "@/features/auth/slices/api";
import { useRouter } from "next/navigation";
import { apiSlice } from "@/core/store/api";
import { instanceAxs } from "@/core/store/conf/baseQuery/axiosInstance";

export const useUser = () => {
  const { wrapAPI } = useWrapAPI();

  const nav = useRouter();

  const dispatch = useDispatch();
  const [mutate, { isLoading: isVoluntaryLoggingOut }] =
    authSliceAPI.useLogoutAuthMutation();

  const loginUser = useCallback(
    (access_token: string) => {
      saveStorage(access_token, { key: "access_token" });
      dispatch(userSlice.actions.login({ access_token }));
    },
    [dispatch]
  );

  const commonLogoutActions = useCallback(() => {
    clearStorage();
    delete instanceAxs.defaults.headers.common.Authorization;
    dispatch(userSlice.actions.logout());
    dispatch(apiSlice.util.resetApiState());
  }, [dispatch]);

  const voluntaryLogoutUser = useCallback(async () => {
    const res = await wrapAPI({
      cbAPI: () => mutate(),
    });

    if (!res) return;

    commonLogoutActions();

    nav.replace("/");
  }, [wrapAPI, mutate, commonLogoutActions, nav]);

  return {
    userState: useGetUserState(),
    loginUser,
    voluntaryLogoutUser,
    isVoluntaryLoggingOut,
    commonLogoutActions,
  };
};
