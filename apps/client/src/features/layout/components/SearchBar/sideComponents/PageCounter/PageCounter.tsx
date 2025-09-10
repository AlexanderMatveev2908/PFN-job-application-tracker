/* eslint-disable @typescript-eslint/no-explicit-any */
/** @jsxImportSource @emotion/react */
"use client";

import { useHydration } from "@/core/hooks/etc/hydration/useHydration";
import { useEffect, useMemo, useState } from "react";
import { useSearchCtxConsumer } from "@/features/layout/components/SearchBar/context/hooks/useSearchCtxConsumer";
import { getMaxBtnForSwap, getNumCardsForPage } from "./uiFactory";
import BtnBg from "../../../../../../common/components/buttons/BtnBg";
import { ArrowBigLeftDash, ArrowBigRightDash } from "lucide-react";
import { css } from "@emotion/react";
import BoxInput from "@/common/components/forms/inputs/BoxInput";
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { __cg } from "@/core/lib/log";
import { v4 } from "uuid";
import { FreshDataArgT } from "../../context/hooks/useSearchCtxProvider";

type PropsType<K extends (...args: any) => any[]> = {
  hook: ReturnType<K>;
};

const PageCounter = <T, K extends (...args: any) => any[]>({
  hook,
}: PropsType<K>) => {
  const { isHydrated } = useHydration();
  const [pagesForSwap, setPagesForSwap] = useState(getMaxBtnForSwap());

  const [triggerRTK, res] = hook;
  const { data: { n_hits = 0, pages = 0 } = {} } = res ?? {};

  const {
    pagination: { swap, page, limit },
    setPagination,
    triggerSearch,
    prevData,
  } = useSearchCtxConsumer();

  useEffect(() => {
    const cb = async () => {
      const newLimit = getNumCardsForPage();
      const newPagesForSwap = getMaxBtnForSwap();

      if (pagesForSwap !== newPagesForSwap) setPagesForSwap(newPagesForSwap);
      if (limit !== newLimit) {
        setPagination({ key: "limit", val: newLimit });

        await triggerSearch({
          freshData: {
            ...(prevData.current ?? {}),
            page: 0,
            limit: newLimit,
          } as FreshDataArgT<T>,
          triggerRTK,
          keyPending: "submit",
          skipCall: true,
        });
      }

      // const newTotPages = Math.ceil(n_hits / newLimit);
      const newTotSwaps = Math.ceil(pages / newPagesForSwap);

      const lastSwapAllowed = Math.max(0, newTotSwaps - 1);
      const lastPageAllowed = Math.max(0, pages - 1);

      const shouldFixPage = page > lastPageAllowed;
      const shouldFixSwap = swap > lastSwapAllowed;

      if (shouldFixPage) setPagination({ key: "page", val: lastPageAllowed });
      if (shouldFixSwap) setPagination({ key: "swap", val: lastSwapAllowed });
    };

    cb();

    window.addEventListener("resize", cb);

    return () => {
      window.removeEventListener("resize", cb);
    };
  }, [
    setPagination,
    n_hits,
    swap,
    page,
    pages,
    limit,
    pagesForSwap,
    triggerSearch,
    triggerRTK,
    prevData,
  ]);

  const totPages = useMemo(() => Math.ceil(n_hits / limit), [limit, n_hits]);
  // const totSwaps = useMemo(
  //   () => Math.ceil(totPages / pagesForSwap),
  //   [totPages, pagesForSwap]
  // );

  const currPages = useMemo(() => {
    const start = swap * pagesForSwap;
    const end = Math.min(start + pagesForSwap, totPages);

    return Array.from({ length: end - start }, (_, i) => start + i).map(
      (int) => ({
        val: int,
        label: int + "",
        id: v4(),
      })
    );
  }, [swap, pagesForSwap, totPages]);

  // __cg(
  //   "pagination",
  //   ["n_hits", n_hits],
  //   ["limit", limit],
  //   ["totPages", totPages],
  //   ["pagesForSwap", pagesForSwap],
  //   ["totSwaps", totSwaps],
  //   ["currPages", currPages],
  //   ["page", page]
  // );

  const handleChangePage = async (val: number) => {
    setPagination({ key: "page", val });

    await triggerSearch({
      freshData: {
        ...(prevData.current ?? {}),
        page: val,
        limit,
      } as FreshDataArgT<T>,
      triggerRTK,
      keyPending: "submit",
      skipCall: true,
    });
  };

  return !isHydrated ? null : (
    <div className="w-full absolute bottom-0 flex justify-center">
      <div className="w-full grid grid-cols-[75px_1fr_75px] gap-10">
        <BtnBg
          {...{
            el: { Svg: ArrowBigLeftDash },
            act: "NONE",
            handleClick: () => setPagination({ key: "swap", val: swap - 1 }),
            isDisabled: !swap,
          }}
        />
        <div
          className="w-full grid justify-items-center gap-6"
          css={css`
            grid-template-columns: repeat(${pagesForSwap}, 1fr);
          `}
        >
          {currPages.map((el) => {
            return (
              <div key={el.id} className="w-[60px]">
                <BoxInput
                  {...{
                    isChosen: el.val === page,
                    handleClick: async () => await handleChangePage(el.val),
                    opt: el,
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
            handleClick: () => setPagination({ key: "swap", val: swap + 1 }),
            isDisabled: (swap + 1) * pagesForSwap > totPages - 1,
          }}
        />
      </div>
    </div>
  );
};

export default PageCounter;
