import { createContext, useContext } from "react";
import { SearchBarCtxT } from "./useSearchCtxProvider";
import { ErrApp } from "@/core/lib/err";

export const SearchBarCtx = createContext<SearchBarCtxT | null>(null);

export const useSearchCtxConsumer = (): SearchBarCtxT => {
  const ctx = useContext<SearchBarCtxT | null>(SearchBarCtx);

  if (!ctx) throw new ErrApp("ctx must be consumed within provider 😡");

  return ctx;
};
