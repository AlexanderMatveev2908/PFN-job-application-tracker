import { FormFieldTxtT } from "@/common/types/ui";
import { FieldValues } from "react-hook-form";
import { v4 } from "uuid";

export type FormFieldIDT<T extends FieldValues> = FormFieldTxtT<T> & {
  id: string;
};

export class FormFieldGen<T extends FieldValues> {
  private genID(): string {
    return v4();
  }

  public txtField(arg: Partial<FormFieldTxtT<T>>): FormFieldIDT<T> {
    return {
      id: this.genID(),
      ...arg,
      place: (arg.place ?? arg.label) + "...",
      type: arg.type ?? "text",
    } as FormFieldIDT<T>;
  }
}
