import { useSelector } from "react-redux";
import { getUserState } from "../slices/slice";
import { REG_JWT } from "@/core/constants/regex";
import { useMemo } from "react";

export const useGetUsState = () => {
  const userState = useSelector(getUserState);

  const isLogged = useMemo(
    () => REG_JWT.test(userState.access_token),
    [userState.access_token]
  );
  const canBePushed = useMemo(
    () => !isLogged && !userState.pendingAction,
    [userState.pendingAction, isLogged]
  );

  return {
    ...userState,
    isLogged,
    canBePushed,
  };
};
