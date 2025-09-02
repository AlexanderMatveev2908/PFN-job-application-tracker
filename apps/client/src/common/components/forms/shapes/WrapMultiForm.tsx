/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import WrapPage from "../../HOC/pageWrappers/WrapPage";
import { ChildrenT } from "@/common/types/ui";
import BtnsSwapper, { PropsTypeBtnsSwapper } from "../../swap/BtnsSwapper";

type PropsType = {
  formTestID: string;
  propsBtnsSwapper: PropsTypeBtnsSwapper;
} & ChildrenT;

const WrapMultiForm: FC<PropsType> = ({
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

          <div className="form__footer">
            <BtnsSwapper
              {...{
                ...propsBtnsSwapper,
              }}
            />
          </div>
        </div>
      </div>
    </WrapPage>
  );
};

export default WrapMultiForm;
