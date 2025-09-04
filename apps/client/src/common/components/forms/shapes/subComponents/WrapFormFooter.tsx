/** @jsxImportSource @emotion/react */
"use client";

import BtnShim from "@/common/components/buttons/BtnShim/BtnShim";
import { isObjOk } from "@/core/lib/dataStructure";
import type { FC } from "react";
import BtnsSwapper, {
  PropsTypeBtnsSwapper,
} from "../swap/subComponents/BtnsSwapper";

type PropsType = {
  propsBtnsSwapper?: PropsTypeBtnsSwapper;
  submitBtnTestID?: string;
  isLoading?: boolean;
};

const WrapFormFooter: FC<PropsType> = ({
  propsBtnsSwapper,
  isLoading,
  submitBtnTestID,
}) => {
  return (
    <div className="cont__grid__lg p-5">
      {isObjOk(propsBtnsSwapper) && (
        <BtnsSwapper
          {...({
            ...propsBtnsSwapper,
          } as PropsTypeBtnsSwapper)}
        />
      )}

      {submitBtnTestID && (
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
      )}
    </div>
  );
};

export default WrapFormFooter;
