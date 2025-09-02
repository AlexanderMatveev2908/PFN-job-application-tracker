/** @jsxImportSource @emotion/react */
"use client";

import BtnShim from "@/common/components/buttons/BtnShim/BtnShim";
import BtnsSwapper, {
  PropsTypeBtnsSwapper,
} from "@/common/components/swap/subComponents/BtnsSwapper";
import { isObjOk } from "@/core/lib/dataStructure";
import type { FC } from "react";

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
    <div className="form__footer">
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
