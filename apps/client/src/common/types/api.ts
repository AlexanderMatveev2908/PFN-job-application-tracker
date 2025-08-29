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

export type HeadersT = {
  "ratelimit-limit": string;
  "ratelimit-remaining": string;
  "ratelimit-window": string;
  "ratelimit-reset": string;
};
export type ConfApiT = {
  url: string;
  params: AxiosRequestConfig["params"];
  responseType: AxiosRequestConfig["responseType"];
  headers: HeadersT;
};
export type DataApiT = {
  msg?: string;
  status?: number;
  isErr?: boolean;
  conf?: ConfApiT;
};

export type BaseQueryReturnT = {
  data: { conf: ConfApiT; status: number; blob?: Blob };
};

export type ResApiT<T> = T extends void
  ? { data: DataApiT }
  : { data: DataApiT & T };
