/* eslint-disable @typescript-eslint/no-explicit-any */
import { AxiosResponseHeaders, RawAxiosResponseHeaders } from "axios";

export const extractHeaders = (
  headers?: AxiosResponseHeaders | RawAxiosResponseHeaders
) => ({
  headers: {
    "ratelimit-limit": headers?.["ratelimit-limit"] ?? null,
    "ratelimit-remaining": headers?.["ratelimit-remaining"] ?? null,
    "ratelimit-window": headers?.["ratelimit-window"] ?? null,
    "ratelimit-reset": headers?.["ratelimit-reset"] ?? null,
  },
});

export const extractMsgErr = (errData: any) =>
  errData?.msg ??
  errData?.message ??
  "A wild Snorlax is fast asleep blocking the road 💤. Try later";
