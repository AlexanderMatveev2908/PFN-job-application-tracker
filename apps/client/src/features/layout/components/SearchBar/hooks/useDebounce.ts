import { useFormContext } from "react-hook-form";
import { useSearchCtxConsumer } from "../context/hooks/useSearchCtxConsumer";
import { useEffect, useRef } from "react";
import { ZodObject } from "zod";
import { isSameObj } from "@/core/lib/dataStructure/ect";
import { clearTmr } from "@/core/lib/etc";
import { useWrapAPI } from "@/core/hooks/api/useWrapAPI";
import { TriggerApiT } from "@/common/types/api";
import { getNumCardsForPage } from "../sideComponents/PageCounter/uiFactory";
import { __cg } from "@/core/lib/log";

type Params<T> = {
  schema: ZodObject;
  triggerRTK: TriggerApiT<T>;
};

export const useDebounce = <T>({ schema, triggerRTK }: Params<T>) => {
  const timerID = useRef<NodeJS.Timeout>(null);

  const {
    prevData,
    setPending,
    triggerSearch,
    api: { skipCall },
  } = useSearchCtxConsumer();
  const { watch } = useFormContext();

  const currForm = watch();

  const { wrapAPI } = useWrapAPI();

  useEffect(() => {
    const merged = {
      ...currForm,
      page: "0",
      limit: getNumCardsForPage(),
    };

    const isFormOk = schema.safeParse(currForm).success;
    if (!isFormOk || timerID.current) return;

    const isSameData = isSameObj(prevData.current, merged);
    if (isSameData) return;

    if (skipCall) {
      __cg("skip api call");
      prevData.current = merged;
      return;
    }

    timerID.current = setTimeout(async () => {
      await triggerSearch({
        freshData: merged,
        triggerRTK,
        keyPending: "submit",
      });
      clearTmr(timerID);
    }, 750);

    return () => {
      clearTmr(timerID);
    };
  }, [
    currForm,
    schema,
    triggerRTK,
    wrapAPI,
    setPending,
    triggerSearch,
    prevData,
    skipCall,
  ]);
};
