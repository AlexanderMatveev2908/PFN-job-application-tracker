import { useEffect, useRef, useState } from "react";
import { useHydration } from "./useHydration";

export type CoordsT = "top" | "left" | "right" | "bottom";
export type CoordsTooltipT = Record<CoordsT, number>;

export const useSyncPortal = () => {
  const parentRef = useRef<HTMLElement | null>(null);
  const [coords, setCoords] = useState<CoordsTooltipT>({
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  });

  const { isHydrated } = useHydration();

  useEffect(() => {
    const el = parentRef.current;
    if (!el || !isHydrated) return;

    const cb = () => {
      const { top, left, right, bottom } = el.getBoundingClientRect();

      setCoords({
        top: top + window.scrollY,
        left: left - el.scrollWidth,
        right: right - el.scrollWidth,
        bottom: bottom + window.scrollY,
      });

      console.log(bottom);
      console.log(window.scrollY);
    };
    cb();

    const ro = new ResizeObserver(cb);
    ro.observe(el);

    window.addEventListener("resize", cb);
    window.addEventListener("scroll", cb);

    return () => {
      ro.disconnect();
      window.removeEventListener("resize", cb);
      window.removeEventListener("scroll", cb);
    };
  }, [isHydrated]);

  return {
    coords,
    parentRef,
  };
};
