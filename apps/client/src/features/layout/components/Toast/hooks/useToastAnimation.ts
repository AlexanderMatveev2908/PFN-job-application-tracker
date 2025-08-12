import { useAnimationControls } from "framer-motion";
import { useCallback, useEffect, useRef } from "react";
import { useSelector } from "react-redux";
import { getToastState } from "../slices";

export const useToastAnimation = () => {
  const toastState = useSelector(getToastState);
  const controls = useAnimationControls();

  const prevX = useRef(toastState.x);
  const prevShown = useRef(false);
  const cancelRef = useRef(false);

  const open = useCallback(async () => {
    controls.stop();
    controls.set("hidden");

    if (cancelRef.current) return;

    await controls.start("open");
  }, [controls]);

  const close = useCallback(async () => {
    controls.stop();

    if (cancelRef.current) return;

    await controls.start("close");
  }, [controls]);

  const closeAndOpen = useCallback(async () => {
    await controls.start("close");

    if (cancelRef.current || !toastState.isShow) return;

    controls.set("hidden");
    if (cancelRef.current) return;

    await controls.start("open");
  }, [controls, toastState.isShow]);

  useEffect(() => {
    cancelRef.current = false;

    if (!toastState.isShow) {
      void close();
      prevShown.current = false;
      prevX.current = toastState.x;
      return () => {
        cancelRef.current = true;
        controls.stop();
      };
    }

    if (prevShown.current && toastState.x !== prevX.current) {
      void closeAndOpen();
    } else {
      void open();
    }

    prevShown.current = true;
    prevX.current = toastState.x;

    return () => {
      cancelRef.current = true;
    };
  }, [toastState.isShow, toastState.x, open, closeAndOpen, close, controls]);

  return { controls };
};
