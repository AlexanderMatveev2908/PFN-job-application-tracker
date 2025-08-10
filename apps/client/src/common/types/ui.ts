import { ReactNode } from "react";
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
