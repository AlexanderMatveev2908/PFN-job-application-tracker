/** @jsxImportSource @emotion/react */
"use client";

import BtnShim from "@/common/components/buttons/BtnShim/BtnShim";
import BtnsSwapper, {
  PropsTypeBtnsSwapper,
} from "@/common/components/swap/BtnsSwapper";
import { isObjOk } from "@/core/lib/dataStructure";
import type { FC } from "react";
import SpannerLinks from "./SpannerLinks/SpannerLinks";

type PropsType = {
  propsBtnsSwapper?: PropsTypeBtnsSwapper;
  isLoading: boolean;
  submitBtnTestID: string;
};

const AuthFormFooter: FC<PropsType> = ({
  propsBtnsSwapper,
  isLoading,
  submitBtnTestID,
}) => {
  return (
    <>
      <div className="w-full grid grid-cols-1 gap-8 p-5">
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
              testID: submitBtnTestID + "__footer_form__submit_btn",
              isLoading,
            }}
          />
        </div>
      </div>
      <SpannerLinks />
    </>
  );
};

export default AuthFormFooter;
