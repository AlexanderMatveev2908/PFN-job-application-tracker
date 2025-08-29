import {
  AxiosRequestConfig,
  AxiosResponseHeaders,
  RawAxiosResponseHeaders,
} from "axios";
import { instanceAxs } from "./axiosInstance";
import { BaseQueryFn } from "@reduxjs/toolkit/query";
import { __cg } from "@/core/lib/log";
import { serialize } from "@/core/lib/dataStructure";
import { BaseQueryReturnT } from "@/common/types/api";

/* eslint-disable @typescript-eslint/no-explicit-any */
type ArgType = {
  url: string;
  method: AxiosRequestConfig["method"];
  data?: AxiosRequestConfig["data"];
  params?: AxiosRequestConfig["params"];
  responseType?: AxiosRequestConfig["responseType"];
};

const extractHeaders = (
  headers: AxiosResponseHeaders | RawAxiosResponseHeaders
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
  data,
  params,
  responseType,
}) => {
  const conf = {
    url: instanceAxs.defaults.baseURL + url,
    params,
    responseType,
    reqData: serialize(data),
  };

  try {
    const {
      data: resData,
      status,
      headers,
    } = await instanceAxs({
      url,
      method,
      data,
      params,
      responseType,
    });

    const confWithHeaders = {
      ...conf,
      ...extractHeaders(headers),
    };

    const result: BaseQueryReturnT = {
      data: {
        conf: confWithHeaders,
        status,
      },
    };

    if (responseType === "blob" && resData instanceof Blob)
      result.data.blob = resData;
    else
      result.data = {
        ...result.data,
        ...resData,
      };

    return result;
  } catch (err: any) {
    const { response } = err ?? {};

    let errData: any = response?.data ?? {};

    if (errData instanceof Blob && errData.type === "application/json") {
      try {
        const text = await errData.text();
        errData = JSON.parse(text);
      } catch (parseErr: any) {
        __cg("Failed parse blob error", parseErr);
      }
    }

    return {
      error: {
        data: {
          conf: {
            ...conf,
            ...extractHeaders(response.headers),
          },
          ...errData,
          msg:
            errData?.msg ??
            errData?.message ??
            "A wild Snorlax is fast asleep blocking the road 💤. Try later",
          status: response?.status ?? 500,
        },
      },
    };
  }
};

export type BaseQueryT = typeof baseQueryAxs;
