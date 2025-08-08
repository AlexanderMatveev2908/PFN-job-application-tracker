import { useCallback } from "react";
import { useHydration } from "../ui/useHydration";

export const useWrapListener = () => {
  const { isHydrated } = useHydration();

  const wrapListener = useCallback(
    (cb: () => void) => {
      if (!isHydrated) return;
      cb();
    },
    [isHydrated]
  );

  return {
    wrapListener,
  };
};
