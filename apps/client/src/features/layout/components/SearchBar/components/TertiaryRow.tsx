/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import MainBtnsSearchBar, {
  MainBtnsSearchBarPropsType,
} from "./subComponents/MainBtnsSearchBar";

type PropsType = {} & MainBtnsSearchBarPropsType;

const TertiaryRow: FC<PropsType> = ({ handleReset }) => {
  return (
    <div className="search_bar__wrap_btns">
      <MainBtnsSearchBar
        {...{
          handleReset,
        }}
      />
    </div>
  );
};

export default TertiaryRow;
