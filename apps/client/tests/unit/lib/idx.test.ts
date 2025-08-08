import { isStr } from "@/core/lib/dataStructure";
import { describe, expect, it } from "vitest";

describe("fn", () => {
  it("check type and structure", () => {
    expect(isStr("abc")).toBe(true);
  });
});
