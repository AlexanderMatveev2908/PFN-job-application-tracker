import { useWrapQuery } from "@/core/hooks/api/useWrapQuery";
import { userSliceAPI } from "../slices/api";
import { useEffect } from "react";
import { isObjOk } from "@/core/lib/dataStructure";
import { useDispatch } from "react-redux";
import { userSlice } from "../slices/slice";
import { getStorage } from "@/core/lib/storage";
import { REG_JWT } from "@/core/constants/regex";

export const useGetUsProfile = () => {
  const dispatch = useDispatch();

  const res = userSliceAPI.useGetProfileQuery(undefined, {
    // skip: !REG_JWT.test(getStorage("access_token") ?? ""),
  });
  const { data, isSuccess } = res;
  useWrapQuery({
    ...res,
  });

  useEffect(() => {
    if (isSuccess && isObjOk(data?.user))
      dispatch(userSlice.actions.setUser(data.user));
  }, [data, isSuccess, dispatch]);
};
