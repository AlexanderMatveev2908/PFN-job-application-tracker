import { ResApiT } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";
import { JobApplicationT } from "../types";

const BASE = "/job-applications";

export const jobApplicationSliceAPI = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    addJobApplication: builder.mutation<
      ResApiT<{ job_application: JobApplicationT }>,
      FormData
    >({
      query: (data) => ({
        url: `${BASE}/`,
        method: "POST",
        data,
      }),
    }),
  }),
});
