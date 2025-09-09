/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { useSearchCtxConsumer } from "../../context/hooks/useSearchCtxConsumer";
import Popup from "@/common/components/wrappers/Popup/Popup";

type PropsType = {};

const SortBar: FC<PropsType> = ({}) => {
  const {
    bars: { sortBar },
    setBar,
  } = useSearchCtxConsumer();

  return (
    <Popup
      {...{
        isPop: sortBar,
        setIsPop: (val: boolean | null) => setBar({ bar: "sortBar", val }),
      }}
    ></Popup>
  );
};

export default SortBar;
