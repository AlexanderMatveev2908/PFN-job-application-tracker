import { useWrapQuery } from "@/core/hooks/api/useWrapQuery";
import { userSliceAPI } from "../slices/api";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { userSlice } from "../slices/slice";

export const useFetchUserProfile = () => {
  const dispatch = useDispatch();

  const res = userSliceAPI.useGetProfileQuery();
  const { data, isSuccess, isError } = res;
  useWrapQuery({
    ...res,
  });

  useEffect(() => {
    if (isSuccess || isError) {
      dispatch(userSlice.actions.setUser(data?.user));
    }
  }, [data, isSuccess, isError, dispatch]);
};
