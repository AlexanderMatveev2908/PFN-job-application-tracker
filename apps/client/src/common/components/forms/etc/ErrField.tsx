/** @jsxImportSource @emotion/react */
"use client";

import { useEffect, useState, type FC } from "react";
import Tooltip from "../../elements/Tooltip";
import { isStr } from "@/core/lib/dataStructure";

type PropsType = {
  msg?: string | null;
};

const ErrField: FC<PropsType> = ({ msg }) => {
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
      }}
    />
  );
};

export default ErrField;
