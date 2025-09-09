import { IconType } from "react-icons";

export type FilterChoiceSearchBarT = {
  val: string;
  label: string;
};

export type FilterSearchBarT = {
  label: string;
  Svg: IconType;
  options: FilterChoiceSearchBarT[];
};
