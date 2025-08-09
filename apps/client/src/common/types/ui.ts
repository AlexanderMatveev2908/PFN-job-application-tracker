import { IconType } from "react-icons";

export interface LinkAppT {
  label: string;
  href: string;
}

export interface LinkAppSvgT extends LinkAppT {
  Svg: IconType;
}

export interface DropMenuT {
  label: string;
  Svg?: IconType;

  links: (LinkAppT | LinkAppSvgT)[];
}
