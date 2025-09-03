import { ResApiT } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";

const BASE = "/verify";

export type VerifyCbcHmacReturnT = {
  cbc_hmac_token?: string;
  access_token?: string;
};

export type VerifyCbcHmacEndpointT =
  | "confirm-email"
  | "recover-pwd"
  | "new-email";

export type VerifyCbcHmacArgT = {
  endpoint: VerifyCbcHmacEndpointT;
  cbc_hmac_token: string;
};

export const verifySliceAPI = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    verifyCbcHmac: builder.query<
      ResApiT<VerifyCbcHmacReturnT>,
      VerifyCbcHmacArgT
    >({
      query: (data) => ({
        url: `${BASE}/${data.endpoint}?cbc_hmac_token=${data.cbc_hmac_token}`,
        method: "GET",
      }),
    }),
  }),
});
