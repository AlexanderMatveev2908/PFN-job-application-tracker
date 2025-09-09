import { CheckChoiceT, FieldCheckT } from "@/common/types/ui";
import { IconType } from "react-icons";

export type FilterSearchBarT = {
  name: string;
  label: string;
  type: FieldCheckT;
  Svg: IconType;
  options: CheckChoiceT[];
};
