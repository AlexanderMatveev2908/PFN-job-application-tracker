/** @jsxImportSource @emotion/react */
"use client";

import { useEffect, useState, type FC } from "react";
import Tooltip from "../../elements/Tooltip/Tooltip";
import { isStr } from "@/core/lib/dataStructure";
import { SerializedStyles } from "@emotion/react";

type PropsType = {
  msg?: string | null;
  $ctmCSS?: SerializedStyles;
};

const ErrField: FC<PropsType> = ({ msg, $ctmCSS }) => {
  const [prevErr, setPrevErr] = useState<string | null>(null);

  useEffect(() => {
    if (isStr(msg) && (!isStr(prevErr) || msg !== prevErr))
      setPrevErr(msg as string);
  }, [prevErr, msg]);

  return (
    <Tooltip
      {...{
        isHover: isStr(msg),
        act: "ERR",
        txt: prevErr,
        $ctmCSS,
      }}
    />
  );
};

export default ErrField;
