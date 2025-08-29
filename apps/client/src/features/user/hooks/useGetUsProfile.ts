import { useWrapQuery } from "@/core/hooks/api/useWrapQuery";
import { userSliceAPI } from "../slices/sliceAPI";
import { useEffect } from "react";
import { isObjOk } from "@/core/lib/dataStructure";
import { useDispatch } from "react-redux";
import { userSlice } from "../slices/slice";

export const useGetUsProfile = () => {
  const dispatch = useDispatch();

  const res = userSliceAPI.useGetProfileQuery();
  const { data, isSuccess } = res;
  useWrapQuery({
    ...res,
  });

  useEffect(() => {
    if (isSuccess && isObjOk(data?.user))
      dispatch(userSlice.actions.setUser(data.user));
  }, [data, isSuccess, dispatch]);
};
