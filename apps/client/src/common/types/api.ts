import { BaseQueryT } from "@/core/store/conf/baseQuery";
import {
  TypedLazyQueryTrigger,
  TypedUseLazyQueryStateResult,
} from "@reduxjs/toolkit/query/react";
import { AxiosRequestConfig } from "axios";

/* eslint-disable @typescript-eslint/no-explicit-any */

export enum TagAPI {
  TEST = "TEST",
  WAKE_UP = "WAKE_UP",
}

export type AppEventT = "OK" | "INFO" | "WARN" | "ERR" | "NONE";

export type ResApiT<T> = {
  data: {
    msg?: string;
    status?: number;
    conf: {
      url: string;
      method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
      params: AxiosRequestConfig["params"];
      responseType: AxiosRequestConfig["responseType"];
    };
  } & T;
};

export type ReqApiT<T extends Record<string, any> | void> = T extends void
  ? {
      _?: number;
    }
  : {
      _?: number;
    } & T;

export type UnwrappedResApiT<T extends void | Record<string, any>> =
  T extends void
    ? { msg?: string; status?: number }
    : { msg?: string; status?: number } & T;

export type ErrApiT<T> = {
  data: { msg?: string; status?: number };
} & T;

export type TriggerTypeRTK<T, K> = TypedLazyQueryTrigger<T, K, BaseQueryT>;
export type ResultTypeRTK<T, K> = TypedUseLazyQueryStateResult<
  T,
  K,
  BaseQueryT
>;
