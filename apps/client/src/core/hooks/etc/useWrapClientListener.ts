import { useCallback } from "react";
import { useHydration } from "../ui/useHydration";

export const useWrapClientListener = () => {
  const { isHydrated } = useHydration();

  const wrapClientListener = useCallback(
    (cb: () => void) => {
      if (!isHydrated) return;
      cb();
    },
    [isHydrated]
  );

  return {
    wrapClientListener,
  };
};
