/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import WrapPage from "../HOC/pageWrappers/WrapPage";
import { ChildrenT } from "@/common/types/ui";
import WrapFormFooter from "../forms/shapes/subComponents/WrapFormFooter";
import { PropsTypeBtnsSwapper } from "./subComponents/BtnsSwapper";

type PropsType = {
  formTestID: string;
  propsBtnsSwapper: PropsTypeBtnsSwapper;
} & ChildrenT;

const WrapMultiFormSwapper: FC<PropsType> = ({
  children,
  formTestID,
  propsBtnsSwapper,
}) => {
  return (
    <WrapPage>
      <div
        data-testid={formTestID + "__form"}
        className="w-full grid grid-cols-1"
      >
        <div className="form__shape">
          {children}

          <WrapFormFooter
            {...{
              propsBtnsSwapper,
            }}
          />
        </div>
      </div>
    </WrapPage>
  );
};

export default WrapMultiFormSwapper;
