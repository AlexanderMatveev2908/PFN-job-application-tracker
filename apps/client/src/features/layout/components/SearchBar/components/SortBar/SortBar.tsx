/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { useSearchCtxConsumer } from "../../context/hooks/useSearchCtxConsumer";
import Popup from "@/common/components/wrappers/Popup/Popup";
import SortBarHeader from "./components/SortBarHeader";
import SortBarBody from "./components/SortBarBody/SortBarBody";
import { SorterSearchBarT } from "../../types";

type PropsType = {
  sorters: SorterSearchBarT[];
};

const SortBar: FC<PropsType> = ({ sorters }) => {
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
    >
      <div className="w-full h-full flex flex-col gap-4">
        <SortBarHeader />

        <SortBarBody {...{ sorters }} />
      </div>
    </Popup>
  );
};

export default SortBar;
