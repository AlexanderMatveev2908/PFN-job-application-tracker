/* eslint-disable @typescript-eslint/no-explicit-any */
/** @jsxImportSource @emotion/react */
"use client";

import { useHydration } from "@/core/hooks/etc/hydration/useHydration";
import { useEffect, useState, type FC } from "react";
import { useSearchCtxConsumer } from "@/features/layout/components/SearchBar/context/hooks/useSearchCtxConsumer";
import { getMaxBtnForSwap } from "./uiFactory";
import BtnBg from "../../../../../../common/components/buttons/BtnBg";
import { ArrowBigLeftDash, ArrowBigRightDash } from "lucide-react";
import { css } from "@emotion/react";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import BoxInput from "@/common/components/forms/inputs/BoxInput";
import { CheckChoiceT } from "@/common/types/ui";
import { keyof } from "zod";

type PropsType = {
  nHits: number;
};

const PageCounter: FC<PropsType> = ({}) => {
  const { isHydrated } = useHydration();
  const [maxBtnsForSwap, setMaxBtnsForSwap] = useState(getMaxBtnForSwap());

  useEffect(() => {
    const cb = () => setMaxBtnsForSwap(getMaxBtnForSwap());

    window.addEventListener("resize", cb);

    return () => {
      window.removeEventListener("resize", cb);
    };
  }, []);

  const {
    pagination: { currBlock, currPage },
    setPagination,
  } = useSearchCtxConsumer();

  const {
    ids: [ids],
  } = useGenIDs({ lengths: [maxBtnsForSwap] });

  return !isHydrated ? null : (
    <div className="w-full absolute bottom-0 flex justify-center">
      <div className="w-full grid grid-cols-[75px_1fr_75px] gap-10">
        <BtnBg
          {...{
            el: { Svg: ArrowBigLeftDash },
            act: "NONE",
          }}
        />
        <div
          className="w-full grid justify-items-center gap-6"
          css={css`
            grid-template-columns: repeat(${maxBtnsForSwap}, 1fr);
          `}
        >
          {ids.map((id, idx) => {
            const opt: CheckChoiceT = {} as CheckChoiceT;
            for (const k of ["label", "val"]) (opt as any)[k] = idx + "";

            return (
              <div key={ids[idx]} className="w-[60px]">
                <BoxInput
                  {...{
                    isChosen: idx === currPage,
                    handleClick: () =>
                      setPagination({ key: "currPage", val: idx }),
                    opt,
                    $labelSizeCls: "lg",
                  }}
                />
              </div>
            );
          })}
        </div>
        <BtnBg
          {...{
            el: { Svg: ArrowBigRightDash },
            act: "NONE",
          }}
        />
      </div>
    </div>
  );
};

export default PageCounter;
