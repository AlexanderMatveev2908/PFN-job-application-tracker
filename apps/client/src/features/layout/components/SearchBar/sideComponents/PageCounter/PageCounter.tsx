/** @jsxImportSource @emotion/react */
"use client";

import { useHydration } from "@/core/hooks/etc/hydration/useHydration";
import { useEffect, useMemo, useState, type FC } from "react";
import { useSearchCtxConsumer } from "@/features/layout/components/SearchBar/context/hooks/useSearchCtxConsumer";
import { getMaxBtnForSwap, getNumCardsForPage } from "./uiFactory";
import BtnBg from "../../../../../../common/components/buttons/BtnBg";
import { ArrowBigLeftDash, ArrowBigRightDash } from "lucide-react";
import { css } from "@emotion/react";
import BoxInput from "@/common/components/forms/inputs/BoxInput";
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { __cg } from "@/core/lib/log";
import { v4 } from "uuid";

type PropsType = {
  nHits: number;
};

const PageCounter: FC<PropsType> = ({ nHits }) => {
  const { isHydrated } = useHydration();
  const [pagesForSwap, setPagesForSwap] = useState(getMaxBtnForSwap());

  const {
    pagination: { currBlock, currPage, limit },
    setPagination,
  } = useSearchCtxConsumer();

  useEffect(() => {
    const cb = () => {
      const newLimit = getNumCardsForPage();
      const newPagesForSwap = getMaxBtnForSwap();

      setPagesForSwap(newPagesForSwap);
      setPagination({ key: "limit", val: newLimit });

      const newTotPages = Math.ceil(nHits / newLimit);
      const newTotSwaps = Math.ceil(newTotPages / newPagesForSwap);

      const lastSwapAllowed = Math.max(0, newTotSwaps - 1);
      const lastPageAllowed = Math.max(0, newTotPages - 1);

      const shouldFixPage = currPage > lastPageAllowed;
      const shouldFixSwap = currBlock > lastSwapAllowed;

      if (shouldFixPage)
        setPagination({ key: "currPage", val: lastPageAllowed });
      if (shouldFixSwap)
        setPagination({ key: "currBlock", val: lastSwapAllowed });
    };

    cb();

    window.addEventListener("resize", cb);

    return () => {
      window.removeEventListener("resize", cb);
    };
  }, [setPagination, nHits, currBlock, currPage]);

  const totPages = useMemo(() => Math.ceil(nHits / limit), [limit, nHits]);
  // const totSwaps = useMemo(
  //   () => Math.ceil(totPages / pagesForSwap),
  //   [totPages, pagesForSwap]
  // );

  const currPages = useMemo(() => {
    const start = currBlock * pagesForSwap;
    const end = Math.min(start + pagesForSwap, totPages);

    return Array.from({ length: end - start }, (_, i) => start + i).map(
      (int) => ({
        val: int,
        label: int + "",
        id: v4(),
      })
    );
  }, [currBlock, pagesForSwap, totPages]);

  // __cg(
  //   "pagination",
  //   ["nHits", nHits],
  //   ["limit", limit],
  //   ["totPages", totPages],
  //   ["pagesForSwap", pagesForSwap],
  //   ["totSwaps", totSwaps],
  //   ["currPages", currPages],
  //   ["currPage", currPage]
  // );

  return !isHydrated ? null : (
    <div className="w-full absolute bottom-0 flex justify-center">
      <div className="w-full grid grid-cols-[75px_1fr_75px] gap-10">
        <BtnBg
          {...{
            el: { Svg: ArrowBigLeftDash },
            act: "NONE",
            handleClick: () =>
              setPagination({ key: "currBlock", val: currBlock - 1 }),
            isDisabled: !currBlock,
          }}
        />
        <div
          className="w-full grid justify-items-center gap-6"
          css={css`
            grid-template-columns: repeat(${pagesForSwap}, 1fr);
          `}
        >
          {currPages.map((page) => {
            return (
              <div key={page.id} className="w-[60px]">
                <BoxInput
                  {...{
                    isChosen: page.val === currPage,
                    handleClick: () =>
                      setPagination({ key: "currPage", val: page.val }),
                    opt: page,
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
            handleClick: () =>
              setPagination({ key: "currBlock", val: currBlock + 1 }),
            isDisabled: (currBlock + 1) * pagesForSwap > totPages - 1,
          }}
        />
      </div>
    </div>
  );
};

export default PageCounter;
