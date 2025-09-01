import { ResApiT } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";
import { EmailFormT } from "../../../core/forms/RequireEmailForm/paperwork";

const BASE = "/require-email";

export type RequireEmailEndpointT = "confirm-email" | "recover-pwd";

export const requireEmailSliceAPI = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    requireEmail: builder.mutation<
      ResApiT<void>,
      EmailFormT & { endpoint: RequireEmailEndpointT }
    >({
      query: (data) => ({
        url: `${BASE}/${data.endpoint}`,
        method: "POST",
        data: {
          email: data.email,
        },
      }),
    }),
  }),
});
