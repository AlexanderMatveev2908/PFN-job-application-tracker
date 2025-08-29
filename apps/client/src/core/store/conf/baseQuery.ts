import {
  AxiosError,
  AxiosRequestConfig,
  AxiosResponseHeaders,
  RawAxiosResponseHeaders,
} from "axios";
import { instanceAxs } from "./axiosInstance";
import { BaseQueryFn } from "@reduxjs/toolkit/query";
import { __cg } from "@/core/lib/log";
import { isStr, serialize } from "@/core/lib/dataStructure";
import { ConfApiT } from "@/common/types/api";
import { saveStorage } from "@/core/lib/storage";

/* eslint-disable @typescript-eslint/no-explicit-any */
type ArgType = {
  url: string;
  method: AxiosRequestConfig["method"];
  data?: AxiosRequestConfig["data"];
  params?: AxiosRequestConfig["params"];
  responseType?: AxiosRequestConfig["responseType"];
};

type BaseQueryReturnT = {
  data: { conf: ConfApiT; status: number; blob?: Blob; refreshed?: boolean };
};

const extractHeaders = (
  headers?: AxiosResponseHeaders | RawAxiosResponseHeaders
) => ({
  headers: {
    "ratelimit-limit": headers?.["ratelimit-limit"] ?? null,
    "ratelimit-remaining": headers?.["ratelimit-remaining"] ?? null,
    "ratelimit-window": headers?.["ratelimit-window"] ?? null,
    "ratelimit-reset": headers?.["ratelimit-reset"] ?? null,
  },
});

export const baseQueryAxs: BaseQueryFn<ArgType, unknown, unknown> = async ({
  url,
  method,
  data: originalDataRequest,
  params,
  responseType,
}) => {
  const conf = {
    url: instanceAxs.defaults.baseURL + url,
    params,
    responseType,
    reqData: serialize(originalDataRequest),
  };

  try {
    const {
      data: responseData,
      status,
      headers,
    } = await instanceAxs({
      url,
      method,
      data: originalDataRequest,
      params,
      responseType,
    });

    const confWithHeaders = {
      ...conf,
      ...extractHeaders(headers),
    };

    const resultReturn: BaseQueryReturnT = {
      data: {
        conf: confWithHeaders,
        status,
      },
    };

    if (responseType === "blob" && responseData instanceof Blob)
      resultReturn.data.blob = responseData;
    else
      resultReturn.data = {
        ...resultReturn.data,
        ...responseData,
      };

    return resultReturn;
  } catch (err: any) {
    const { response } = (err ?? {}) as AxiosError<any>;

    const status = response?.status;
    let errData: any = response?.data ?? {};

    if (errData instanceof Blob && errData.type === "application/json") {
      try {
        const text = await errData.text();
        errData = JSON.parse(text);
      } catch (parseErr: any) {
        __cg("Failed parse blob error", parseErr);
      }
    }

    if (
      status === 401 &&
      ["jwt_expired", "jwt_invalid", "jwt_not_provided"].some((txt) =>
        (errData?.msg ?? "")?.includes(txt)
      )
    ) {
      const { data } = await instanceAxs.get("/auth/refresh");

      const access_token = data?.access_token;

      if (isStr(access_token)) {
        saveStorage(access_token, { key: "access_token" });

        instanceAxs.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${access_token}`;

        const {
          data: dataRetry,
          status,
          headers,
        } = await instanceAxs({
          url,
          method,
          data: originalDataRequest,
          params,
          responseType,
        });

        const confWithHeaders = {
          ...conf,
          ...extractHeaders(headers),
        };

        __cg("refresh access");

        const resultRetryReturn: BaseQueryReturnT = {
          data: {
            conf: confWithHeaders,
            status,
            refreshed: true,
          },
        };

        if (responseType === "blob" && dataRetry instanceof Blob)
          resultRetryReturn.data.blob = dataRetry;
        else
          resultRetryReturn.data = {
            ...resultRetryReturn.data,
            ...dataRetry,
          };
      }
    }

    return {
      error: {
        data: {
          conf: {
            ...conf,
            ...extractHeaders(response?.headers),
          },
          ...errData,
          msg:
            errData?.msg ??
            errData?.message ??
            "A wild Snorlax is fast asleep blocking the road 💤. Try later",
          status,
        },
      },
    };
  }
};

export type BaseQueryT = typeof baseQueryAxs;
