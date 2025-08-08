import { formatDate } from "./formatters";

/* eslint-disable @typescript-eslint/no-explicit-any */
export const __cg = (title: string, ...args: any[]) => {
  console.group(title.toUpperCase());

  for (const el of args) {
    console.log(el);
  }

  console.groupEnd();

  const trace = new Error();
  const traces = trace.stack?.split("\n");

  let firstTrace: string | undefined;
  for (const t of traces ?? []) {
    if (t.includes("src")) {
      firstTrace = t;
      break;
    }
  }

  const path = firstTrace?.split("src")?.[1];

  console.log(`=> ${path} 🚀 \n ${formatDate(Date.now())} 🕰️`);
};
