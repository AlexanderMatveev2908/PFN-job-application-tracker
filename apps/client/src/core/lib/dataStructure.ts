/* eslint-disable @typescript-eslint/no-explicit-any */
export const isStr = (str: unknown): boolean =>
  typeof str === "string" && !!str.trim().length;

export const isObjOk = (obj: any, cb?: (v: any) => boolean): boolean =>
  typeof obj === "object" &&
  obj !== null &&
  !!Object.keys(obj).length &&
  Object.values(obj).some((v) => (typeof cb === "function" ? cb(v) : true));

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

export function serialize(
  v: unknown,
  seen: WeakSet<any> = new WeakSet()
): JSONValT {
  if (
    v === null ||
    typeof v === "string" ||
    typeof v === "number" ||
    typeof v === "boolean"
  )
    return v;

  if (typeof v === "bigint") return v + "";
  if (
    typeof v === "function" ||
    typeof v === "symbol" ||
    typeof v === "undefined"
  )
    return `=> ${typeof v}`;

  if (v instanceof Date) return v.toISOString();

  if (Array.isArray(v)) {
    if (seen.has(v)) throw new Error("circular reference detected");
    seen.add(v);
    return v.map((item) => serialize(item, seen));
  }

  if (v instanceof Map) {
    if (seen.has(v)) throw new Error("circular reference detected");
    seen.add(v);

    const obj: Record<string, JSONValT> = {};

    for (const [k, vv] of v.entries()) {
      obj[serialize(k, seen) + ""] = serialize(vv, seen);
    }
    return obj;
  }

  if (v instanceof Set) {
    if (seen.has(v)) throw new Error("circular reference detected");
    seen.add(v);
    return Array.from(v).map((item) => serialize(item, seen));
  }

  if (typeof v === "object") {
    if (seen.has(v)) throw new Error("circular reference detected");
    seen.add(v);
    const obj: Record<string, JSONValT> = {};
    for (const [k, vv] of Object.entries(v)) {
      obj[k] = serialize(vv, seen);
    }
    return obj;
  }

  return null;
}
