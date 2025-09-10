import { useFormContext } from "react-hook-form";
import { useSearchCtxConsumer } from "../context/hooks/useSearchCtxConsumer";
import { useEffect, useRef } from "react";
import { ZodObject } from "zod";
import { cpyObj, isSameObj } from "@/core/lib/dataStructure/ect";
import { clearTmr } from "@/core/lib/etc";
import { useWrapAPI } from "@/core/hooks/api/useWrapAPI";
import { TriggerApiT } from "@/common/types/api";
import { getNumCardsForPage } from "../sideComponents/PageCounter/uiFactory";

type Params<T> = {
  schema: ZodObject;
  triggerRTK: TriggerApiT<T>;
};

export const useDebounce = <T>({ schema, triggerRTK }: Params<T>) => {
  const timerID = useRef<NodeJS.Timeout>(null);

  const { prevData, setPending, triggerSearch } = useSearchCtxConsumer();
  const { watch } = useFormContext();

  const currForm = watch();

  const { wrapAPI } = useWrapAPI();

  useEffect(() => {
    const merged = cpyObj({
      ...currForm,
      page: "0",
      limit: getNumCardsForPage(),
    });

    const isFormOk = schema.safeParse(currForm).success;
    if (!isFormOk || timerID.current) return;

    const isSameData = isSameObj(prevData.current, merged);
    if (isSameData) return;

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
    prevData,
    schema,
    triggerRTK,
    wrapAPI,
    setPending,
    triggerSearch,
  ]);
};
