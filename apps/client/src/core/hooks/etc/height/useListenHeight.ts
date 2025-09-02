/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useRef, useState } from "react";

type Params = {
  opdDep?: any[];
};

export const useListenHeight = ({ opdDep }: Params) => {
  const contentRef = useRef<HTMLDivElement>(null);
  const [contentH, setContentH] = useState(0);

  useEffect(() => {
    const el = contentRef.current;
    if (!el) return;

    const cb = () => setContentH(el.offsetHeight + 50);
    cb();

    const ro = new ResizeObserver(cb);
    ro.observe(el);

    window.addEventListener("resize", cb);
    return () => {
      ro.disconnect();
      window.removeEventListener("resize", cb);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...(opdDep ?? [])]);

  return {
    contentRef,
    contentH,
  };
};
