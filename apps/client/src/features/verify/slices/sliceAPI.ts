import { ResApiT } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";

const BASE_URL = "/verify";

export type VerifyUserReturnT = {
  cbc_hmac_token?: string;
  access_token?: string;
};

export const verifySliceAPI = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    confEmail: builder.query<ResApiT<VerifyUserReturnT>, string>({
      query: (cbc_hmac_token) => ({
        url: `${BASE_URL}/confirm-email?cbc_hmac_token=${cbc_hmac_token}`,
        method: "GET",
      }),
    }),
  }),
});
