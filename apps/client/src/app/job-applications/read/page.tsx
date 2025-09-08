/** @jsxImportSource @emotion/react */
"use client";

import SearchBar from "@/features/layout/components/SearchBar/SearchBar";
import type { FC } from "react";

const Page: FC = () => {
  return (
    <div className="page__shape">
      <SearchBar />
    </div>
  );
};

export default Page;
