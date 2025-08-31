import { instanceAxs } from "./axiosInstance";
import { BaseQueryFn } from "@reduxjs/toolkit/query";
import { serialize } from "@/core/lib/dataStructure";
import { ArgType, BaseQueryReturnT } from "./lib/types";
import { extractHeaders, extractMsgErr, parseErr } from "./lib/etc";
import { handleRefreshErr, refreshToken } from "./lib/refresh";
import { getStorage } from "@/core/lib/storage";

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
    jwt: getStorage("access_token") as string,
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

    const resultReturn: BaseQueryReturnT = {
      data: {
        conf: {
          ...conf,
          ...extractHeaders(headers),
        },
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
    const { response, errData, status = 500 } = await parseErr(err);

    if (
      status !== 401 ||
      !["jwt_expired", "jwt_invalid", "jwt_not_provided"].some((txt) =>
        (errData?.msg ?? "")?.includes(txt)
      ) ||
      response?.config?.url === "/auth/refresh"
    )
      return {
        error: {
          ...errData,
          conf: {
            ...conf,
            ...extractHeaders(response?.headers),
          },
          msg: extractMsgErr(errData),
          status,
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
