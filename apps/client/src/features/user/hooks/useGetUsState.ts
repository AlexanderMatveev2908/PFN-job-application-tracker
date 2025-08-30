import { useSelector } from "react-redux";
import { getUserState } from "../slices/slice";
import { REG_JWT } from "@/core/constants/regex";

export const useGetUsState = () => {
  const userState = useSelector(getUserState);

  const isLogged = REG_JWT.test(userState.access_token);

  return {
    ...userState,
    isLogged,
    canBePushed: !isLogged && !userState.pendingAction,
  };
};
