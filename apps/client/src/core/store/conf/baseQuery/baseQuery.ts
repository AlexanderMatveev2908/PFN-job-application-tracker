import { AxiosError } from "axios";
import { instanceAxs } from "./axiosInstance";
import { BaseQueryFn } from "@reduxjs/toolkit/query";
import { __cg } from "@/core/lib/log";
import { serialize } from "@/core/lib/dataStructure";
import { ArgType, BaseQueryReturnT } from "./lib/types";
import { extractHeaders, extractMsgErr } from "./lib/etc";
import { handleRefreshErr, refreshToken } from "./lib/refresh";

/* eslint-disable @typescript-eslint/no-explicit-any */

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

    const confWithHeaders = {
      ...conf,
      ...extractHeaders(response?.headers),
    };
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
      status !== 401 ||
      !["jwt_expired", "jwt_invalid", "jwt_not_provided"].some(
        (txt) =>
          (errData?.msg ?? "")?.includes(txt) ||
          response?.config?.url === "/auth/refresh"
      )
    )
      return {
        error: {
          data: {
            ...errData,
            conf: confWithHeaders,
            msg: extractMsgErr(errData),
            status,
          },
        },
      };

    try {
      return await refreshToken({
        url,
        method,
        params,
        responseType,
        conf,
        data: originalDataRequest,
      });
    } catch (err: any) {
      return handleRefreshErr({ err, conf });
    }
  }
};

export type BaseQueryT = typeof baseQueryAxs;
