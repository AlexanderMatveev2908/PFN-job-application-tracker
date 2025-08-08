import { clearTmr } from "@/core/lib/etc";
import { toastSlice } from "../slices";
import { useCallback, useEffect, useRef } from "react";
import { DispatchT } from "@/core/store";
import { ToastStateT } from "../types";
import { useWrapListener } from "@/core/hooks/etc/useWrapListener";

export const useToastStages = ({
  dispatch,
  toastState,
}: {
  dispatch: DispatchT;
  toastState: ToastStateT;
}) => {
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const prevStatus = useRef<boolean>(false);
  const prevID = useRef<string>("");
  const forcingRef = useRef<boolean>(false);

  const { wrapListener } = useWrapListener();

  const clickClose = useCallback(() => {
    dispatch(toastSlice.actions.close());
    clearTmr(timerRef);
    prevStatus.current = false;
  }, [dispatch]);

  useEffect(() => {
    const listen = () => {
      if (
        !toastState.isShow ||
        prevStatus.current ||
        forcingRef.current ||
        prevID.current === toastState.id
      )
        return;

      // __cg("stage 1 ");

      clearTmr(timerRef);

      prevID.current = toastState.id;
      prevStatus.current = true;

      timerRef.current = setTimeout(() => {
        if (
          !toastState.isShow ||
          forcingRef.current ||
          !prevStatus.current ||
          prevID.current !== toastState.id
        )
          return;

        clickClose();
      }, 4000);
    };

    wrapListener(listen);

    // ? cleanup
    return () => {
      clearTmr(timerRef);
    };
  }, [wrapListener, toastState.isShow, clickClose, toastState.id]);

  useEffect(() => {
    const listen = () => {
      if (
        !toastState.isShow ||
        !prevStatus.current ||
        forcingRef.current ||
        prevID.current === toastState.id
      )
        return;

      // __cg("stage 2");

      clearTmr(timerRef);

      prevStatus.current = false;
      forcingRef.current = true;

      dispatch(toastSlice.actions.close());
    };

    wrapListener(listen);
  }, [
    wrapListener,
    toastState.isShow,
    toastState.toast,
    toastState.id,
    dispatch,
  ]);

  useEffect(() => {
    const listen = () => {
      if (
        !forcingRef.current ||
        toastState.isShow ||
        prevStatus.current ||
        prevID.current === toastState.id
      )
        return;

      // __cg("stage 3");

      clearTmr(timerRef);

      forcingRef.current = false;

      timerRef.current = setTimeout(() => {
        if (
          toastState.isShow ||
          forcingRef.current ||
          prevStatus.current ||
          prevID.current === toastState.id
        )
          return;

        clearTmr(timerRef);
        dispatch(toastSlice.actions.force());
      }, 400);
    };

    wrapListener(listen);

    return () => {
      clearTmr(timerRef);
    };
  }, [wrapListener, toastState.isShow, dispatch, toastState.id]);

  return {
    clickClose,
  };
};
