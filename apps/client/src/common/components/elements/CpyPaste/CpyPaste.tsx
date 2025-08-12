/** @jsxImportSource @emotion/react */
"use client";

import {
  useEffect,
  useReducer,
  useRef,
  type CSSProperties,
  type FC,
} from "react";
import CpyClip from "./components/CpyClip";
import { clearTmr } from "@/core/lib/etc";
import { __cg } from "@/core/lib/log";
import { reducer } from "./atc/reducer";
import { initState } from "./atc/initState";

type PropsType = {
  txt: string;
};

const CpyPaste: FC<PropsType> = ({ txt }) => {
  const [state, dispatchRCT] = useReducer(reducer, initState);
  const btnRef = useRef<HTMLButtonElement | null>(null);
  const prevData = useRef({
    id: "",
    isCopied: false,
    forcing: false,
  });
  const timerID = useRef<NodeJS.Timeout>(null);

  useEffect(() => {
    const el = btnRef.current;
    if (!el) return;

    if (
      !state.isCopied ||
      prevData.current.id === state.id ||
      prevData.current.isCopied
    )
      return;

    const cb = () => {
      clearTmr(timerID);

      prevData.current = {
        ...state,
        forcing: false,
      };
      timerID.current = setTimeout(() => {
        prevData.current.isCopied = false;
        dispatchRCT({ type: "CLOSE" });
        clearTmr(timerID);
      }, 1500);
    };

    cb();

    return () => {
      clearTmr(timerID);
    };
  }, [state]);

  useEffect(() => {
    if (!prevData.current.isCopied || prevData.current.id === state.id) return;

    const cb = () => {
      clearTmr(timerID);
      prevData.current = {
        isCopied: false,
        id: state.id,
        forcing: true,
      };

      dispatchRCT({ type: "CLOSE" });
    };

    cb();
  }, [state]);

  useEffect(() => {
    if (
      !prevData.current.forcing ||
      state.isCopied ||
      state.id === prevData.current.id
    )
      return;

    const cb = () => {
      clearTmr(timerID);
      prevData.current.forcing = false;

      timerID.current = setTimeout(() => {
        clearTmr(timerID);
        dispatchRCT({ type: "FORCE" });
      }, 300);
    };

    cb();
  }, [state]);

  const handleClick = async () => {
    try {
      await navigator.clipboard.writeText(txt);
      dispatchRCT({ type: "OPEN" });
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (err: any) {
      __cg("cpy err", err);
    }
  };

  return (
    <button
      onClick={handleClick}
      ref={btnRef}
      type="button"
      className="btn__app w-fit py-2 px-4 border-2 border-w__0 rounded-xl relative"
      style={
        {
          "--scale__up": 1.15,
        } as CSSProperties
      }
    >
      <CpyClip {...{ isCopied: state.isCopied }} />

      <span className="txt__md">{txt}</span>
    </button>
  );
};

export default CpyPaste;
