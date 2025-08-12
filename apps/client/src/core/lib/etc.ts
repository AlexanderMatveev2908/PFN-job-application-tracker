import { RefObject } from "react";

export const clearTmr = (timerID: RefObject<NodeJS.Timeout | null>) => {
  if (!timerID.current) return;

  clearTimeout(timerID.current);
  timerID.current = null;
};

export const isWdw = () => typeof window !== "undefined";

export const genASCI = () => {
  const upper = Array.from({ length: 26 }, (_, i) =>
    String.fromCharCode(65 + i)
  );
  const lower = Array.from({ length: 26 }, (_, i) =>
    String.fromCharCode(97 + i)
  );
  const nums = Array.from({ length: 10 }, (_, i) => i);

  const ranges: [number, number][] = [
    [33, 47],
    [58, 64],
    [91, 96],
    [123, 126],
  ];

  const symbols = ranges.flatMap(([a, b]) =>
    Array.from({ length: b - a + 1 }, (_, i) => String.fromCharCode(a + i))
  );

  return {
    upper,
    lower,
    nums,
    symbols,
  };
};

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

export const genIdx = (n: number): number => {
  const MAX = 2 ** 32;

  const limit = MAX - (MAX % n);
  const buf = new Uint32Array(1);

  let v: number;
  do {
    crypto.getRandomValues(buf);
    v = buf[0];
  } while (v >= limit);

  return v % n;
};

export const shuffle = (arg: string): string => {
  const arr = arg.split("");

  let i = arg.length - 1;

  while (i > 0) {
    const j = genIdx(i + 1);
    [arr[i], arr[j]] = [arr[j], arr[i]];
    i--;
  }

  return arr.join("");
};

export const genPwd = () => {
  const { upper, lower, nums, symbols } = genASCI();
  let pwd = "";

  for (const r of [lower, upper, nums, symbols]) {
    let j = 0;
    while (j < 4) {
      const idx = genIdx(r.length);
      pwd += r[idx];

      j++;
    }
  }

  return shuffle(pwd);
};
