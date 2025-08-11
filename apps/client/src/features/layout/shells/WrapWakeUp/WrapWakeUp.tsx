/** @jsxImportSource @emotion/react */
"use client";

import { useCallback, useEffect, useRef, useState, type FC } from "react";
import WrapPop from "@/common/components/HOC/WrapPop/WrapPop";
import { useWrapListener } from "@/core/hooks/etc/useWrapListener";
import { wakeUpSliceAPI } from "./slices/api";
import { useWrapQuery } from "@/core/hooks/api/useWrapQuery";
import { clearTmr } from "@/core/lib/etc";
import { getStorage, saveStorage } from "@/core/lib/storage";
import { useHydration } from "@/core/hooks/ui/useHydration";
import SpinBtn from "@/common/components/spinners/SpinBtn";
import { isStr } from "@/core/lib/dataStructure";

type PropsType = {
  children: React.ReactNode;
};

const WrapWakeUp: FC<PropsType> = ({ children }) => {
  const [isPop, setIsPop] = useState<boolean | null>(null);
  const [canGo, setCanGo] = useState(false);

  const isAwakeRef = useRef<boolean>(false);
  const timerID = useRef<NodeJS.Timeout | null>(null);

  const { wrapListener } = useWrapListener();
  const { isHydrated } = useHydration();

  const [triggerRTK, res] = wakeUpSliceAPI.useLazyWakeServerQuery();
  const { triggerRef } = useWrapQuery({
    ...res,
    showToast: true,
  });
  const triggerAPI = useCallback(async () => {
    triggerRef();
    const resAPI = await triggerRTK(
      {
        _: Date.now(),
      },
      false
    );

    return resAPI.data;
  }, [triggerRef, triggerRTK]);

  useEffect(() => {
    const listener = () => {
      const lastVal = getStorage("WAKE_UP");

      const delta = Date.now() - +(lastVal ?? 0);
      const min = delta / 1000 / 60;

      setCanGo(true);

      if (min < 15) {
        isAwakeRef.current = true;
        return;
      }

      isAwakeRef.current = false;
      setIsPop(true);
    };

    wrapListener(listener);
  }, [wrapListener, isHydrated]);

  useEffect(() => {
    const listener = async () => {
      if (!canGo) return;

      let count = 0;
      while (!isAwakeRef.current) {
        await new Promise<void>((resPrm) => {
          timerID.current = setTimeout(
            async () => {
              try {
                const r = await triggerAPI();

                if (isStr(r?.msg)) {
                  saveStorage(Date.now(), { key: "WAKE_UP" });
                  isAwakeRef.current = true;
                  setIsPop(false);
                } else {
                  count++;
                }
              } catch {
                count++;
              }

              clearTmr(timerID);
              resPrm();
            },
            count ? 2000 : 0
          );
        });
      }
    };

    wrapListener(listener);

    return () => {
      clearTmr(timerID);
    };
  }, [triggerAPI, triggerRTK, canGo, wrapListener]);

  return (
    <div className="w-full h-full pt-[25px] pb-[200px] px-[25px] sm:px-[50px]">
      <WrapPop
        {...{
          isPop,
          setIsPop,
          allowClose: false,
        }}
      >
        <div className="w-full h-[75%] flex flex-col items-center justify-center gap-20">
          <span className="txt__lg text-neutral-200">
            Server waking up ... 💤
          </span>

          <SpinBtn />
        </div>
      </WrapPop>

      {children}
    </div>
  );
};

export default WrapWakeUp;
