import { UnwrappedResApiT } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";

const BASE_URL = "/verify";

export const verifySliceAPI = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    confEmail: builder.query<
      UnwrappedResApiT<{ cbc_hmac_token?: string; access_token?: string }>,
      string
    >({
      query: (cbc_hmac_token) => ({
        url: `${BASE_URL}/confirm-email?cbc_hmac_token=${cbc_hmac_token}`,
        method: "GET",
      }),
    }),
  }),
});
