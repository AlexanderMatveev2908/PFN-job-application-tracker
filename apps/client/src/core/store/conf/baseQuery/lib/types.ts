import { ConfApiT } from "@/common/types/api";
import { AxiosRequestConfig } from "axios";

export type ArgType = {
  url: string;
  method: AxiosRequestConfig["method"];
  data?: AxiosRequestConfig["data"];
  params?: AxiosRequestConfig["params"];
  responseType?: AxiosRequestConfig["responseType"];
};

export type BaseQueryReturnT = {
  data: { conf: ConfApiT; status: number; blob?: Blob; refreshed?: boolean };
};
