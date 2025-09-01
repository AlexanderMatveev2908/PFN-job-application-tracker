import { ResApiT, TagAPI } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";
import { userSlice } from "@/features/user/slices/slice";

const BASE_URL = "/verify";

export type VerifyConfEmailReturnT = {
  cbc_hmac_token?: string;
  access_token?: string;
};

export type VerifyRecoverPwdReturnT = {
  cbc_hmac_token?: string;
};

export const verifySliceAPI = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    verifyConfEmail: builder.query<ResApiT<VerifyConfEmailReturnT>, string>({
      query: (cbc_hmac_token) => ({
        url: `${BASE_URL}/confirm-email?cbc_hmac_token=${cbc_hmac_token}`,
        method: "GET",
      }),
      async onQueryStarted(_, { dispatch, queryFulfilled }) {
        try {
          await queryFulfilled;

          dispatch(apiSlice.util.invalidateTags([TagAPI.USER]));
        } catch {}
      },
    }),
    verifyRecoverPwd: builder.query<ResApiT<VerifyRecoverPwdReturnT>, string>({
      query: (cbc_hmac_token) => ({
        url: `${BASE_URL}/recover-pwd?cbc_hmac_token=${cbc_hmac_token}`,
        method: "GET",
      }),

      async onQueryStarted(arg, { dispatch, queryFulfilled }) {
        try {
          await queryFulfilled;
          dispatch(userSlice.actions.setCbcHmac(arg));
        } catch {}
      },
    }),
  }),
});
