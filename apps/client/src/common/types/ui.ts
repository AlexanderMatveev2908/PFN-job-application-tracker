import { ReactNode } from "react";
import { FieldValues, Path } from "react-hook-form";
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
  place: string;
  type: FieldInputT;
  label?: string | null;
};
