import { useEffect, useRef, useState } from "react";
import { useHydration } from "./useHydration";

export const useSyncPortal = () => {
  const parentRef = useRef<HTMLElement | null>(null);
  const [coords, setCoords] = useState([0, 0]);

  const { isHydrated } = useHydration();

  useEffect(() => {
    const el = parentRef.current;
    if (!el || !isHydrated) return;

    const cb = () => {
      const { top, left } = el.getBoundingClientRect();

      setCoords([top + window.scrollY, left - el.scrollWidth]);

      // console.log(top);
      // console.log(window.scrollY);

      console.log(left);
      console.log(el.scrollWidth);
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
