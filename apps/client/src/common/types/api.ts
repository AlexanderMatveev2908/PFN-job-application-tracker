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

export type ReqApiT<T extends Record<string, any> | void> = T extends void
  ? {
      _?: number;
    }
  : {
      _?: number;
    } & T;

type ConfApiT = {
  url: string;
  method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  params: AxiosRequestConfig["params"];
  responseType: AxiosRequestConfig["responseType"];
};
type DataApiT = {
  msg: string;
  status?: number;
  conf: ConfApiT;
  isErr?: boolean;
};
export type ResApiT<T> = T extends void
  ? { data: DataApiT }
  : { data: DataApiT & T };

export type UnwrappedResApiT<T> = ResApiT<T>["data"];

export type TriggerRTKT<T, K> = TypedLazyQueryTrigger<
  T,
  ResApiT<K>,
  BaseQueryT
>;
export type ResultRTKT<T, K> = TypedUseLazyQueryStateResult<
  T,
  ResApiT<K>,
  BaseQueryT
>;
