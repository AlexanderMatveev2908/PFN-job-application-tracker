/* eslint-disable @typescript-eslint/no-explicit-any */
export const isStr = (str: unknown): boolean =>
  typeof str === "string" && !!str.trim().length;

export const isObjOk = (obj: any, cb?: (v: any) => boolean): boolean =>
  typeof obj === "object" &&
  obj !== null &&
  !!Object.keys(obj).length &&
  Object.values(obj).some((v) => (typeof cb === "function" ? cb(v) : true));

export const isArrOk = (arr: any, cb?: (v: any) => boolean) =>
  Array.isArray(arr) &&
  arr.length &&
  arr.every((el) => (typeof cb === "function" ? cb(el) : true));
