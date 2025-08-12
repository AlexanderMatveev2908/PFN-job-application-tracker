/** @jsxImportSource @emotion/react */
"use client";

import {
  RefObject,
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
import { useSyncPortal } from "@/core/hooks/ui/useSyncPortal";
import { PortalConfT } from "@/common/types/ui";

type PropsType = { txt: string; portalConf?: PortalConfT };

const CpyPaste: FC<PropsType> = ({ txt, portalConf }) => {
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

  const { coords, parentRef } = useSyncPortal(portalConf?.optDep);

  return (
    <button
      ref={parentRef as RefObject<HTMLButtonElement>}
      onClick={handleClick}
      type="button"
      className="btn__app w-fit py-2 px-4 border-2 border-w__0 rounded-xl relative"
      style={{ "--scale__up": 1.15 } as CSSProperties}
    >
      {(portalConf?.showPortal ?? true) && (
        <CpyClip {...{ ...state, coords }} />
      )}
      <span className="txt__md">{txt}</span>
    </button>
  );
};

export default CpyPaste;
