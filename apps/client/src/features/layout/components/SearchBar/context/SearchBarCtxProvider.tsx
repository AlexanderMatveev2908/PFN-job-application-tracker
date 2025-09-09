/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import { createContext, type FC } from "react";
import {
  SearchBarCtxT,
  useSearchCtxProvider,
} from "./hooks/useSearchCtxProvider";

export const SearchBarCtx = createContext<SearchBarCtxT | null>(null);

const SearchBarCtxProvider: FC<ChildrenT> = ({ children }) => {
  return (
    <SearchBarCtx.Provider value={useSearchCtxProvider()}>
      {children}
    </SearchBarCtx.Provider>
  );
};

export default SearchBarCtxProvider;
