/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useRef, useState } from "react";
import { useHydration } from "./useHydration";

export type CoordsT = "top" | "left" | "right" | "bottom";
export type CoordsTooltipT = Record<CoordsT, number>;

type PropsType = {
  optDep?: any[];
};

export const useSyncPortal = (params: PropsType = {}) => {
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
      const { top, left, right, bottom, width } = el.getBoundingClientRect();

      setCoords({
        top: top + window.scrollY,
        left: left - width,
        right: right - width,
        bottom: bottom + window.scrollY,
      });
    };

    console.log(window.scrollX);
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isHydrated, ...(params.optDep ?? [])]);

  return {
    coords,
    parentRef,
  };
};
