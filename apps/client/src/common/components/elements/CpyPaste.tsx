/** @jsxImportSource @emotion/react */
"use client";

import type { CSSProperties, FC } from "react";

type PropsType = {
  txt: string;
};

const CpyPaste: FC<PropsType> = ({ txt }) => {
  return (
    <button
      type="button"
      className="btn__app w-fit py-2 px-4 border-2 border-w__0 rounded-xl"
      style={
        {
          "--scale__up": 1.15,
        } as CSSProperties
      }
    >
      <span className="txt__md">{txt}</span>
    </button>
  );
};

export default CpyPaste;
