import { ChangeEvent, ReactNode, RefObject } from "react";
import { Control, FieldValues, Path } from "react-hook-form";
import { IconType } from "react-icons";

export interface LinkAppT {
  label: string;
  href: string;
}

export interface LinkAppSvgT extends LinkAppT {
  Svg: IconType;
  fill?: string;
  stroke?: string;
}

export interface FieldTxtSvgT {
  label?: string;
  Svg?: IconType;
}

export type ChildrenT = {
  children: ReactNode;
};

export type FieldInputT = "text" | "email" | "password" | "url" | "textarea";

export type FormFieldTxtT<T extends FieldValues> = {
  name: Path<T>;
  label: string | null;
  place: string;
  type: FieldInputT;
};

export type FormFieldSvgT<T extends FieldValues> = FormFieldTxtT<T> & {};

export type FieldCheckT = "checkbox" | "radio";

export type FormFieldCheckT<T extends FieldValues> = {
  name: Path<T>;
  label: string | null;
  type: FieldCheckT;
};

export type PortalConfT = {
  showPortal: boolean;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  optDep?: any[];
};

export type RawFieldPropsT<T extends FieldValues> = {
  el: FormFieldTxtT<T>;
  control: Control<T>;
  cbChange?: (v: string) => void;
  cbFocus?: (v: string) => void;
  cbBlur?: (v: string) => void;
  isDisabled?: boolean;
  manualMsg?: string;
  showLabel?: boolean;
  dynamicInputT?: FieldInputT;
  optRef?: RefObject<HTMLElement | null>;
  portalConf?: PortalConfT;
};

export type RawEventT = ChangeEvent<HTMLInputElement | HTMLTextAreaElement>;

export type TestIDT = {
  t_id?: string;
};
