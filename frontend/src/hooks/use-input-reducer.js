import { useReducer } from "react";

const initialInputState = {
  value: "",
  isTouched: false,
};

const inputStateReducer = (prevState, action) => {
  if (action.type === "INPUT") {
    return { value: action.payload, isTouched: prevState.isTouched };
  }
  if (action.type === "BLUR") {
    return { value: prevState.value, isTouched: true };
  }
  if (action.type === "RESET") {
    return { value: "", isTouched: false };
  }

  return initialInputState;
};

const useInput = (validateValueFn) => {
  const [inputState, dispatch] = useReducer(inputStateReducer, initialInputState);

  const isValueValid = validateValueFn(inputState.value);
  const hasError = !isValueValid && inputState.isTouched;

  const changeValueHandler = (event) => {
    dispatch({type: "INPUT", payload: event.target.value });
  };

  const blurInputHandler = (event) => {
    dispatch({type: "BLUR"});
  };
  
  const reset = () => {
    dispatch({type: "RESET"});
  };

  return {
    value: inputState.value,
    isValid: isValueValid,
    hasError,
    changeValueHandler,
    blurInputHandler,
    reset,
  }
};

export default useInput;