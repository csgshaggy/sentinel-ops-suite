import React, { useRef, useState, useEffect } from "react";
import { HStack, PinInput, PinInputField, FormControl, FormLabel } from "@chakra-ui/react";

interface TotpInputProps {
  label?: string;
  onComplete: (code: string) => void;
  autoFocus?: boolean;
}

const TotpInput: React.FC<TotpInputProps> = ({ label = "Authentication Code", onComplete, autoFocus = true }) => {
  const [value, setValue] = useState("");
  const inputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    if (autoFocus && inputRef.current) {
      inputRef.current.focus();
    }
  }, [autoFocus]);

  const handleChange = (val: string) => {
    setValue(val);
    if (val.length === 6) {
      onComplete(val);
    }
  };

  return (
    <FormControl>
      {label && <FormLabel>{label}</FormLabel>}

      <HStack spacing={2}>
        <PinInput
          otp
          value={value}
          onChange={handleChange}
          type="number"
          manageFocus
        >
          <PinInputField ref={inputRef} />
          <PinInputField />
          <PinInputField />
          <PinInputField />
          <PinInputField />
          <PinInputField />
        </PinInput>
      </HStack>
    </FormControl>
  );
};

export default TotpInput;
