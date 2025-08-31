import { useDispatch } from "react-redux";
import { userSlice } from "../slices/slice";
import { useCallback } from "react";
import { clearStorage, saveStorage } from "@/core/lib/storage";
import { useGetUserState } from "./useGetUserState";
import { useWrapAPI } from "@/core/hooks/api/useWrapAPI";
import { authSliceAPI } from "@/features/auth/slices/api";
import { useRouter } from "next/navigation";

export const useUser = () => {
  const { wrapAPI } = useWrapAPI();

  const nav = useRouter();

  const dispatch = useDispatch();
  const [mutate, { isLoading: isLoadingLoggingOut }] =
    authSliceAPI.useLogoutUserMutation();

  const loginUser = useCallback(
    (access_token: string) => {
      saveStorage(access_token, { key: "access_token" });
      dispatch(userSlice.actions.login({ access_token }));
    },
    [dispatch]
  );

  const logoutUser = useCallback(async () => {
    const res = await wrapAPI({
      cbAPI: () => mutate(),
    });

    if (res.isErr) return;

    clearStorage();
    dispatch(userSlice.actions.logout());

    nav.replace("/");
  }, [wrapAPI, mutate, dispatch, nav]);

  return {
    userState: useGetUserState(),
    loginUser,
    logoutUser,
    isLoadingLoggingOut,
  };
};
