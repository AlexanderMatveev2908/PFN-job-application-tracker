import { useCallback } from "react";
import { useDispatch } from "react-redux";
import { userSlice } from "../slices/slice";
import { saveStorage } from "@/core/lib/storage";

export const useSaveCbcHmac = () => {
  const dispatch = useDispatch();

  const saveCbcHmac = useCallback(
    (cbc_hmac_token: string) => {
      dispatch(userSlice.actions.setCbcHmac(cbc_hmac_token));
      saveStorage(cbc_hmac_token, { key: "cbc_hmac_token" });
    },
    [dispatch]
  );

  return {
    saveCbcHmac,
  };
};
