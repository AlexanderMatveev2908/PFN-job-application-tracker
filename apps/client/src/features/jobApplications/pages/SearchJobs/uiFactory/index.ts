import { FilterSearchBarT } from "@/features/layout/components/SearchBar/types";
import {
  applicationStatusChoices,
  companyNameField,
  positionNameField,
} from "../../../uiFactory";
import { IoStatsChart } from "react-icons/io5";

export const searchJobsFieldsTxt = [companyNameField, positionNameField];

export const filtersSearchJobs: FilterSearchBarT[] = [
  {
    label: "Status",
    Svg: IoStatsChart,
    options: applicationStatusChoices,
  },
];
