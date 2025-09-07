import { AadCbcHmacT } from "@/common/types/tokens";
import { REG_CBC_HMAC } from "../constants/regex";
import { ErrApp } from "./err";

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

export const isSerializable = (
  v: any,
  seen: WeakSet<any> = new WeakSet()
): boolean => {
  if (
    v === null ||
    typeof v === "string" ||
    typeof v === "number" ||
    typeof v === "boolean"
  )
    return true;

  if (typeof v === "bigint" || typeof v === "function" || typeof v === "symbol")
    return false;

  if (v instanceof Date) return true;
  if (v instanceof FormData) return false;
  if (v instanceof Map || v instanceof Set) return false;

  if (typeof v === "object") {
    if (seen.has(v)) return false;
    seen.add(v);

    return Object.values(v).every((v) => isSerializable(v, seen));
  }

  return false;
};

type JSONValT =
  | string
  | number
  | boolean
  | null
  | JSONValT[]
  | { [key: string]: JSONValT };

export const serialize = (
  data: unknown,
  seen: WeakSet<any> = new WeakSet()
): JSONValT => {
  if (
    data === null ||
    typeof data === "string" ||
    typeof data === "number" ||
    typeof data === "boolean"
  )
    return data;

  if (typeof data === "bigint") return data + "";
  if (
    typeof data === "function" ||
    typeof data === "symbol" ||
    typeof data === "undefined"
  )
    return `=> ${typeof data}`;

  if (data instanceof Date) return data.toISOString();

  if (Array.isArray(data)) {
    if (seen.has(data)) throw new ErrApp("circular reference detected");
    seen.add(data);
    return data.map((item) => serialize(item, seen));
  }

  if (data instanceof Map) {
    if (seen.has(data)) throw new ErrApp("circular reference detected");
    seen.add(data);

    const obj: Record<string, JSONValT> = {};

    for (const [k, vv] of data.entries()) {
      obj[JSON.stringify(serialize(k, seen))] = serialize(vv, seen);
    }
    return obj;
  }

  if (data instanceof Set) {
    if (seen.has(data)) throw new ErrApp("circular reference detected");
    seen.add(data);
    return Array.from(data).map((item) => serialize(item, seen));
  }

  if (data instanceof FormData) {
    if (seen.has(data)) throw new ErrApp("circular reference detected");
    seen.add(data);

    const obj: Record<string, JSONValT> = {};

    for (const [k, v] of data.entries()) {
      obj[k] = serialize(v);
    }

    return obj;
  }

  if (typeof data === "object") {
    if (seen.has(data)) throw new ErrApp("circular reference detected");
    seen.add(data);
    const obj: Record<string, JSONValT> = {};
    for (const [k, vv] of Object.entries(data)) {
      obj[k] = serialize(vv, seen);
    }
    return obj;
  }

  return null;
};

export const hexToBytes = (hex: string) => {
  const arg = new Uint8Array(hex.length / 2);

  let i = 0;

  while (i < arg.length) {
    arg[i] = parseInt(hex.substring(i * 2, i * 2 + 2), 16);
    i++;
  }

  return arg;
};

export const hexToDict = (hex: string) =>
  JSON.parse(new TextDecoder().decode(hexToBytes(hex)));

export const extractAadFromCbcHmac = (
  cbc_hmac_token?: string | null
): AadCbcHmacT | null => {
  let aad: AadCbcHmacT | null = null;
  try {
    if (cbc_hmac_token && REG_CBC_HMAC.test(cbc_hmac_token))
      aad = hexToDict(cbc_hmac_token!.split(".")[0]!);
  } catch {
    aad = null;
  }

  return aad;
};

export const hexToRgb = (hex: string): string => {
  let clean = hex.replace("#", "").toLowerCase();

  if (clean.length === 3)
    clean = clean
      .split("")
      .map((ch) => ch + ch)
      .join("");

  const match = clean.match(/.{2}/g);
  if (!match || match.length < 3) {
    throw new ErrApp(`Invalid hex color: ${hex}`);
  }

  const [r, g, b] = match.map((x) => parseInt(x, 16));

  return `rgb(${r}, ${g}, ${b})`;
};

const ALPHB32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

export const b32ToHex = (str: string) => {
  let buffer = 0;
  let bitsLeft = 0;
  const output = [];

  for (const char of str.replace(/=+$/, "")) {
    const idx = ALPHB32.indexOf(char.toUpperCase());
    if (idx === -1) throw new ErrApp("Invalid b32 => " + char);

    buffer = (buffer << 5) | idx;
    bitsLeft += 5;

    if (bitsLeft >= 8) {
      bitsLeft -= 8;
      output.push((buffer >> bitsLeft) & 0xff);
    }
  }

  return output.map((b) => b.toString(16).padStart(2, "0")).join("");
};

const ALPHB64 =
  "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

export const b64ToHex = (str: string) => {
  let buffer = 0;
  let bitsLeft = 0;
  const output = [];

  for (const char of str.replace(/=+$/, "")) {
    const idx = ALPHB64.indexOf(char);
    if (idx === -1) throw new ErrApp("Invalid b64 => " + char);

    buffer = (buffer << 6) | idx;
    bitsLeft += 6;

    if (bitsLeft >= 8) {
      bitsLeft -= 8;
      output.push((buffer >> bitsLeft) & 0xff);
    }
  }
  return output.map((b) => b.toString(16).padStart(2, "0")).join("");
};
