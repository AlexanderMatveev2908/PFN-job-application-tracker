import { RefObject } from "react";

export const clearTmr = (timerID: RefObject<NodeJS.Timeout | null>) => {
  if (!timerID.current) return;

  clearTimeout(timerID.current);
  timerID.current = null;
};

export const isWdw = () => typeof window !== "undefined";

export const genLorem = (n?: number) =>
  "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Exercitationem perferendis nostrum, sapiente dicta praesentium neque ratione rem facilis. Alias quos libero vel iusto quam in, recusandae accusamus cupiditate fugiat nam.".repeat(
    n ?? 1
  );

export const calcIsCurrPath = (path: string, href: string) => {
  const noQuery = path.split(/[?#]/).shift();
  const base = noQuery!.replace(/\/+$/, "");

  const escaped = base.replace(/[.*+?^${}()|\\[\]]/g, "\\$&");

  const reg = new RegExp(`^${escaped}(?:/+)?(?:\\?.*)?$`);

  return reg.test(href);
};

export const genMinMax = (min: number, max: number) =>
  Math.floor(Math.random() * (max - min + 1) + min);
