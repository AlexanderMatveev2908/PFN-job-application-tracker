import { AppEventT } from "@/common/types/api";
import { IconType } from "react-icons";
import { FaSearch } from "react-icons/fa";
import { FaEraser } from "react-icons/fa6";

export type MainBtnSearchBarT = {
  Svg: IconType;
  label?: string;
  act: AppEventT;
};

const searchBtn: MainBtnSearchBarT = {
  Svg: FaSearch,
  label: "Search",
  act: "OK",
};

const eraseBtn: MainBtnSearchBarT = {
  Svg: FaEraser,
  label: "Reset",
  act: "ERR",
};

export const mainBtnsSearchBar = [searchBtn, eraseBtn];
