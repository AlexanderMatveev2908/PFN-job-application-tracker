import { uiBreaks } from "@/core/constants/uiBreaks";
import { isWdw } from "@/core/lib/etc";

{
}
export const getColsForSwap = () => {
  if (!isWdw()) return 1;

  const w = window.innerWidth;

  return w > uiBreaks.lg ? 4 : w > uiBreaks.md ? 3 : w > uiBreaks.sm ? 2 : 1;
};
