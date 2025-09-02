/** @jsxImportSource @emotion/react */
"use client";

import BtnShim from "@/common/components/buttons/BtnShim/BtnShim";
import BtnsSwapper, {
  PropsTypeBtnsSwapper,
} from "@/common/components/swap/BtnsSwapper";
import { isObjOk } from "@/core/lib/dataStructure";
import type { FC } from "react";
import SpannerLinks from "../../../../../features/auth/components/SpannerLinks/SpannerLinks";

type PropsType = {
  propsBtnsSwapper?: PropsTypeBtnsSwapper;
  isLoading: boolean;
  submitBtnTestID: string;
};

const WrapFormFooter: FC<PropsType> = ({
  propsBtnsSwapper,
  isLoading,
  submitBtnTestID,
}) => {
  return (
    <>
      <div className="form__footer">
        {isObjOk(propsBtnsSwapper) && (
          <BtnsSwapper
            {...({
              ...propsBtnsSwapper,
            } as PropsTypeBtnsSwapper)}
          />
        )}

        <div className="w-[250px] justify-self-center">
          <BtnShim
            {...{
              type: "submit",
              label: "Submit",
              testID: submitBtnTestID + "__form__submit",
              isLoading,
            }}
          />
        </div>
      </div>
      <SpannerLinks />
    </>
  );
};

export default WrapFormFooter;
