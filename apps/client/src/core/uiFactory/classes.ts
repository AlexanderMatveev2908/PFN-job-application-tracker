import { FormFieldTxtT } from "@/common/types/ui";
import { FieldValues } from "react-hook-form";
import { v4 } from "uuid";
import { captAll } from "../lib/formatters";

export type FormFieldIDT<T extends FieldValues> = FormFieldTxtT<T> & {
  id: string;
};

export class FormFieldGen<T extends FieldValues> {
  private genID(): string {
    return v4();
  }

  public txtField(arg: Partial<FormFieldTxtT<T>>): FormFieldIDT<T> {
    const label = arg.label ?? captAll(arg.name!.replace(/_/g, " "));

    return {
      id: this.genID(),
      ...arg,
      label,
      place: (arg.place ?? label) + "...",
      type: arg.type ?? "text",
    } as FormFieldIDT<T>;
  }
}
