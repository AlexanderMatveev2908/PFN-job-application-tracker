/* eslint-disable @typescript-eslint/no-explicit-any */
import { UserT } from "@/features/user/types";
import { isObjOk, isStr } from "./dataStructure";

export const formatDate = (date: Date | string | number) => {
  const param =
    date instanceof Date
      ? date
      : /^\d{10,}n?$/.test(date + "")
      ? +date
      : new Date(date);

  return new Intl.DateTimeFormat("en-US", {
    hour: "numeric",
    minute: "numeric",
    second: "numeric",

    hour12: true,
  }).format(param);
};

export const capt = (str?: string) =>
  str ? str?.[0]?.toUpperCase() + str?.slice(1) : "";

export const captAll = (str?: string) =>
  !str
    ? ""
    : str
        .split(" ")
        .filter(Boolean)
        .map((el) => capt(el))
        .join(" ");

export const extractInitialsUser = (user: UserT) =>
  user.first_name[0].toUpperCase() + user.last_name[0].toUpperCase();

export const parseDevValUsFriendly = (v: string) =>
  captAll(v.split("_").join(" ").toLowerCase());

export const defValDatePicker = () => new Date().toISOString().split("T")[0];

export const fromPickerToTmst = (v: string) =>
  new Date(v + "T00:00:00Z").getTime();

export const genFormData = (
  obj: any,
  formData: FormData = new FormData(),
  prefix = ""
): FormData => {
  for (const [k, v] of Object.entries(obj)) {
    if (v === undefined) continue;

    const key = prefix ? `${prefix}[${k}]` : k;

    if (Array.isArray(v)) {
      const arrayKey = key + "[]";
      for (const vv of v) {
        if (isObjOk(vv)) {
          genFormData(vv, formData, arrayKey);
        } else {
          formData.append(arrayKey, isStr(vv) ? vv : vv + "");
        }
      }
    } else if (isObjOk(v)) {
      genFormData(v, formData, key);
    } else {
      formData.append(key, (isStr(v) ? v : v + "") as string);
    }
  }

  return formData;
};

export const logFormData = (formData: FormData) => {
  for (const [k, v] of formData.entries()) {
    console.log(`🔑 ${k} => 💎 ${v}`);
  }
};
