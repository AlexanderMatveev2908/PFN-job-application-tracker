import { AxiosRequestConfig } from "axios";
import { instanceAxs } from "./axiosInstance";
import { BaseQueryFn } from "@reduxjs/toolkit/query";
import { __cg } from "@/core/lib/log";

/* eslint-disable @typescript-eslint/no-explicit-any */
type ArgType = {
  url: string;
  method: AxiosRequestConfig["method"];
  data?: AxiosRequestConfig["data"];
  params?: AxiosRequestConfig["params"];
  responseType?: AxiosRequestConfig["responseType"];
};

export const baseQueryAxs: BaseQueryFn<ArgType, unknown, unknown> = async ({
  url,
  method,
  data,
  params,
  responseType,
}) => {
  try {
    const { data: resData, status } = await instanceAxs({
      url,
      method,
      data,
      params,
      responseType,
    });

    return responseType === "blob" && resData instanceof Blob
      ? {
          data: {
            blob: resData,
            status,
          },
        }
      : {
          data: {
            ...resData,
            status,
          },
        };
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
        config: {
          url: instanceAxs.defaults.baseURL + url,
          params,
          responseType,
          data: !(data instanceof FormData) ? data : null,
        },

        data: {
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
