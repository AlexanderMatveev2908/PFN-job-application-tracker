import { ResApiT } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";
import { EmailFormT } from "../components/RequireEmailForm/paperwork";

const BASE = "/require-email";

export const requireEmailSliceAPI = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    requireConfEmail: builder.mutation<ResApiT<void>, EmailFormT>({
      query: (data) => ({
        url: `${BASE}/confirm-email`,
        method: "POST",
        data,
      }),
    }),
  }),
});
