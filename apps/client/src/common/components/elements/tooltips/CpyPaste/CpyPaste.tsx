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
import { reducer } from "./etc/reducer";
import { initState } from "./etc/initState";
import { clearTmr } from "@/core/lib/etc";
import { useSyncPortal } from "@/core/hooks/ui/useSyncPortal";
import { PortalConfT, TestIDT } from "@/common/types/ui";

type PropsType = { txt: string; portalConf?: PortalConfT } & TestIDT;

const CpyPaste: FC<PropsType> = ({ txt, portalConf, testID }) => {
  const [state, dispatch] = useReducer(reducer, initState);
  const timerID = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (!state.isCopied) return;
    clearTmr(timerID);

    timerID.current = setTimeout(() => dispatch({ type: "CLOSE" }), 1600);

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
      data-testid={testID}
      ref={parentRef as RefObject<HTMLButtonElement>}
      onClick={handleClick}
      type="button"
      className="btn__app w-fit py-2 px-4 border-2 border-w__0 rounded-xl relative"
      style={{ "--scale__up": 1.15 } as CSSProperties}
    >
      {(portalConf?.showPortal ?? true) && (
        <CpyClip {...{ ...state, coords }} />
      )}
      <span data-testid="cpy_paste__result" className="txt__md">
        {txt}
      </span>
    </button>
  );
};

export default CpyPaste;
