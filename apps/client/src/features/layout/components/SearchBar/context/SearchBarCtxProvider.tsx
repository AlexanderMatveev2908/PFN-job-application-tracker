/** @jsxImportSource @emotion/react */
"use client";

import { ChildrenT } from "@/common/types/ui";
import type { FC } from "react";
import { SearchBarCtx } from "./hooks/ctxConsumer";
import { useSearchCtxProvider } from "./hooks/useSearchCtxProvider";

const SearchBarCtxProvider: FC<ChildrenT> = ({ children }) => {
  return (
    <SearchBarCtx.Provider value={useSearchCtxProvider()}>
      {children}
    </SearchBarCtx.Provider>
  );
};

export default SearchBarCtxProvider;
