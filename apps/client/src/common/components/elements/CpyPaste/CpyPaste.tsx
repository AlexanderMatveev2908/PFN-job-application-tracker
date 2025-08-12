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
import { __cg } from "@/core/lib/log";
import { reducer } from "./atc/reducer";
import { initState } from "./atc/initState";
import { clearTmr } from "@/core/lib/etc";

type PropsType = { txt: string };

const CpyPaste: FC<PropsType> = ({ txt }) => {
  const [state, dispatch] = useReducer(reducer, initState);
  const timerID = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (!state.isCopied) return;
    clearTmr(timerID);

    timerID.current = setTimeout(() => dispatch({ type: "CLOSE" }), 1500);

    return () => {
      clearTmr(timerID);
    };
  }, [state.isCopied, state.x]);

  const handleClick = async () => {
    try {
      await navigator.clipboard.writeText(txt);
      dispatch({ type: "OPEN" });
    } catch (err) {
      __cg("cpy err", err);
    }
  };

  return (
    <button
      onClick={handleClick}
      type="button"
      className="btn__app w-fit py-2 px-4 border-2 border-w__0 rounded-xl relative"
      style={{ "--scale__up": 1.15 } as CSSProperties}
    >
      <CpyClip {...state} />
      <span className="txt__md">{txt}</span>
    </button>
  );
};

export default CpyPaste;
