import { useFormContext } from "react-hook-form";
import { useSearchCtxConsumer } from "../context/hooks/useSearchCtxConsumer";
import { useEffect } from "react";
import { ZodObject } from "zod";

type Params = {
  schema: ZodObject;
};

export const useDebounce = ({ schema }: Params) => {
  const { prevForm } = useSearchCtxConsumer();
  const { watch } = useFormContext();

  const currForm = watch();

  useEffect(() => {}, []);

  return {};
};
