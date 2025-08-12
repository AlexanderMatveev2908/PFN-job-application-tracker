import { useAnimationControls } from "framer-motion";
import { useCallback, useEffect, useRef } from "react";
import { useSelector } from "react-redux";
import { getToastState } from "../slices";

export const useToastAnimation = () => {
  const toastState = useSelector(getToastState);

  const controls = useAnimationControls();

  const prevX = useRef(toastState.x);
  const prevShown = useRef(false);

  const open = useCallback(async () => {
    controls.stop();
    controls.set("hidden");
    await controls.start("open");
  }, [controls]);

  const closeAndOpen = useCallback(
    async (cancelled: boolean) => {
      await controls.start("close");
      if (cancelled || !toastState.isShow) return;

      controls.set("hidden");
      await controls.start("open");
    },
    [controls, toastState.isShow]
  );

  useEffect(() => {
    let cancelled = false;

    if (!toastState.isShow) {
      prevShown.current = false;
      prevX.current = toastState.x;
      return;
    }

    const changedX = toastState.x !== prevX.current;

    if (prevShown.current && changedX) {
      void closeAndOpen(cancelled);
    } else {
      void open();
    }

    prevShown.current = true;
    prevX.current = toastState.x;

    return () => {
      cancelled = true;
    };
  }, [toastState.isShow, toastState.x, controls, open, closeAndOpen]);

  return {
    controls,
  };
};
