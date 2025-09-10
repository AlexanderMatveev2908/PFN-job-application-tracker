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

export const cpyObj = <T>(obj: T): T => {
  if (obj === null || typeof obj !== "object") return obj;

  if (typeof obj === "function") return obj as T;

  if (obj instanceof Date) return new Date(obj.getTime()) as T;

  if (obj instanceof RegExp) return new RegExp(obj.source, obj.flags) as T;

  if (obj instanceof Set)
    return new Set(Array.from(obj, (v) => cpyObj(v))) as T;

  if (obj instanceof Map)
    return new Map(
      Array.from(obj.entries(), ([k, v]) => [cpyObj(k), cpyObj(v)])
    ) as T;

  if (Array.isArray(obj)) return obj.map((v) => cpyObj(v)) as T;

  const cpy: Record<string, unknown> = {};
  for (const k in obj)
    if (Object.prototype.hasOwnProperty.call(obj, k)) cpy[k] = cpyObj(obj[k]);

  return cpy as T;
};

export const isSameObj = <T>(objA: T, objB: T): boolean => {
  if (objA === objB) return true;

  if ([objA, objB].some((el) => el === null || typeof el !== "object"))
    return false;

  if (objA instanceof Date && objB instanceof Date)
    return objA.getTime() === objB.getTime();

  if (objA instanceof RegExp && objB instanceof RegExp)
    return objA.source === objB.source && objA.flags === objB.flags;

  if (Array.isArray(objA) && Array.isArray(objB)) {
    if (objA.length !== objB.length) return false;
    return objA.every((val, i) => isSameObj(val, objB[i]));
  }

  if (objA instanceof Set && objB instanceof Set) {
    if (objA.size !== objB.size) return false;
    return [...objA].every((val) => [...objB].some((v) => isSameObj(val, v)));
  }

  if (objA instanceof Map && objB instanceof Map) {
    if (objA.size !== objB.size) return false;
    return [...objA.entries()].every(
      ([k, v]) => objB.has(k) && isSameObj(v, objB.get(k))
    );
  }

  const keysA = Object.keys(objA as Record<string, unknown>);
  const keysB = Object.keys(objB as Record<string, unknown>);
  if (keysA.length !== keysB.length) return false;

  return keysA.every((k) =>
    isSameObj(
      (objA as Record<string, unknown>)[k],
      (objB as Record<string, unknown>)[k]
    )
  );
};
