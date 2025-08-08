import { RefObject } from "react";

export const clearTmr = (timerID: RefObject<NodeJS.Timeout | null>) => {
  if (!timerID.current) return;

  clearTimeout(timerID.current);
  timerID.current = null;
};

export const isWdw = () => typeof window !== "undefined";
