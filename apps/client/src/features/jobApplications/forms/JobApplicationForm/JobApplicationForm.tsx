/** @jsxImportSource @emotion/react */
"use client";

import type { FC } from "react";
import { useFormContext } from "react-hook-form";
import { JobApplicationFormT } from "../../paperwork";
import { txtFieldsApplicationForm } from "./uiFactory";
import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import BtnShim from "@/common/components/buttons/BtnShim/BtnShim";
import { useFocus } from "@/core/hooks/etc/focus/useFocus";

type PropsType = {
  handleSave: () => void;
};

const JobApplicationForm: FC<PropsType> = ({ handleSave }) => {
  const { control, setFocus } = useFormContext<JobApplicationFormT>();

  const testID = "job_application";

  useFocus("company_name", { setFocus });

  return (
    <form
      data-testid={`${testID}__form`}
      onSubmit={handleSave}
      className="page__shape"
    >
      <div className="cont__grid__lg">
        {txtFieldsApplicationForm.map((el) => (
          <FormFieldTxt
            key={el.id}
            {...{
              el,
              control,
            }}
          />
        ))}
      </div>

      <div className="w-[250px] mx-auto mt-[50px]">
        <BtnShim
          {...{
            type: "submit",
            label: "Submit",
            testID: `${testID}__form__submit`,
          }}
        />
      </div>
    </form>
  );
};

export default JobApplicationForm;
