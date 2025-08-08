import { UnwrappedResApiT } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";

const BASE_URL = "/test/";

export const testSliceAPI = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getHello: builder.query<UnwrappedResApiT<void>, void>({
      query: () => ({
        url: BASE_URL,
        method: "GET",
      }),
    }),

    posHello: builder.mutation<UnwrappedResApiT<void>, { msg: string }>({
      query: ({ msg }) => ({
        url: BASE_URL,
        method: "POST",
        data: { msg },
      }),
    }),
  }),
});
