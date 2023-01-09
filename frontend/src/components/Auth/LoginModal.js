import { useContext, useEffect } from "react";

import AuthContext from "../../store/auth-context";
import { login as apiLogin } from "../../lib/api";
import validateEmail from "../../lib/validation";

import Button from "../UI/Button";
import Input from "../UI/Input";
import LoadingSpinner from "../UI/LoadingSpinner";
import Modal from "../UI/Modal";

import useInput from "../../hooks/use-input-reducer";
import useHttp from "../../hooks/use-http";

import logoImg from "../../assets/logo.png";
import styles from "./LoginModal.module.css";

const LoginModal = (props) => {
  const authCtx = useContext(AuthContext);

  const {
    sendRequest,
    status: requestStatus,
    data: authData,
    error: serverError,
  } = useHttp(apiLogin);

  const {
    value: emailValue,
    isValid: emailIsValid,
    hasError: emailHasError,
    changeValueHandler: emailChangeHandler,
    blurInputHandler: emailBlurHandler,
  } = useInput(validateEmail);

  const {
    value: passwordValue,
    isValid: passwordIsValid,
    hasError: passwordHasError,
    changeValueHandler: passwordChangeHandler,
    blurInputHandler: passwordBlurHandler,
  } = useInput((val) => val.trim() !== "" && val.length && val.length > 5);

  const isFormValid = emailIsValid && passwordIsValid;

  const formSubmitHandler = (event) => {
    event.preventDefault();

    if (!isFormValid) {
      return;
    }

    const loginData = JSON.stringify({
      email: emailValue,
      password: passwordValue
    })

    sendRequest(loginData);
  }

  const { onClose } = props;

  useEffect(() => {
    if (requestStatus === "completed" && !serverError) {
      authCtx.login(authData);

      onClose();
    } 
  }, [requestStatus, serverError, authData, authCtx, onClose]);

  let hasServerError = false;
  if (requestStatus === "completed" && serverError) {
    hasServerError = true;
  }

  return (
    <Modal onClose={props.onClose}>
      <div className={styles["signin-modal"]}>
        <form onSubmit={formSubmitHandler} className={styles["signin"]}>
          <img className={styles["signin-image"]} src={logoImg} alt="Login" />
          {hasServerError && (
            <span className={styles["error-text"]}>{serverError}</span>
          )}
          {emailHasError && (
            <span className={styles["error-text"]}>
              Email must follow a format 'name@some.domain'
            </span>
          )}
          <Input
            hasError={emailHasError}
            id="email"
            placeholder="email"
            type="text"
            onChange={emailChangeHandler}
            onBlur={emailBlurHandler}
            value={emailValue}
          />
          {passwordHasError && (
            <span className={styles["error-text"]}>
              Password must be min 6 characters long
            </span>
          )}
          <Input
            hasError={passwordHasError}
            id="password"
            placeholder="password"
            type="password"
            onChange={passwordChangeHandler}
            onBlur={passwordBlurHandler}
            value={passwordValue}
          />
          <Button type="submit" disabled={!isFormValid}>
            Login
          </Button>
        </form>
        {requestStatus === "pending" && (
          <div className="centered">
            <LoadingSpinner />
          </div>
        )}
      </div>
    </Modal>
  );
}

export default LoginModal;