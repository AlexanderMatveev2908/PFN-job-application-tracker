import { useCallback } from "react";
import { useDispatch } from "react-redux";
import { userSlice } from "../../../../features/user/slices/slice";
import { delStorageItm, saveStorage } from "@/core/lib/storage";

export const useManageCbcHmac = () => {
  const dispatch = useDispatch();

  const saveCbcHmac = useCallback(
    (cbc_hmac_token: string) => {
      dispatch(userSlice.actions.setCbcHmac(cbc_hmac_token));
      saveStorage(cbc_hmac_token, { key: "cbc_hmac_token" });
    },
    [dispatch]
  );

  const delCbcHmac = useCallback(() => {
    delStorageItm("cbc_hmac_token");
    dispatch(userSlice.actions.clearCbcHmac());
  }, [dispatch]);

  return {
    saveCbcHmac,
    delCbcHmac,
  };
};
