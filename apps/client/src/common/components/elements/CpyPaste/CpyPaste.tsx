/** @jsxImportSource @emotion/react */
"use client";

import {
  useEffect,
  useRef,
  useState,
  type CSSProperties,
  type FC,
} from "react";
import CpyClip from "./components/CpyClip";
import { clearTmr } from "@/core/lib/etc";
import { __cg } from "@/core/lib/log";

type PropsType = {
  txt: string;
};

const CpyPaste: FC<PropsType> = ({ txt }) => {
  const [isCopied, setIsCopied] = useState(false);
  const btnRef = useRef<HTMLButtonElement | null>(null);
  const timerID = useRef<NodeJS.Timeout>(null);

  useEffect(() => {
    const el = btnRef.current;
    if (!el) return;

    if (isCopied)
      timerID.current = setTimeout(() => {
        setIsCopied(false);

        clearTmr(timerID);
      }, 1000);

    return () => {
      clearTmr(timerID);
    };
  }, [isCopied]);

  const handleClick = async () => {
    try {
      await navigator.clipboard.writeText(txt);
      setIsCopied(true);
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
      <CpyClip {...{ isCopied }} />

      <span className="txt__md">{txt}</span>
    </button>
  );
};

export default CpyPaste;
