import { useContext, useEffect } from "react";

import AuthContext from "../../store/auth-context";
import { addComment as apiAddComment } from "../../lib/api";
import useInput from "../../hooks/use-input-reducer";
import useHttp from "../../hooks/use-http";

import Button from "../UI/Button";
import Input from "../UI/Input";

import styles from "./NewCommentForm.module.css";

const NewCommentForm = (props) => {
  const authCtx = useContext(AuthContext);

  const {
    sendRequest,
    status: requestStatus,
    error: serverError,
  } = useHttp(apiAddComment);

  const {
    value: commentValue,
    isValid: commentIsValid,
    changeValueHandler: commentChangeHandler,
    blurInputHandler: commentBlurHandler,
    reset: resetComment,
  } = useInput((val) => val.trim() !== "" && val.length);

  const { onAddedComment } = props;

  useEffect(() => {
    if (requestStatus === "completed" && !serverError) {
      onAddedComment();
    } 
  }, [requestStatus, serverError, onAddedComment]);

  const isFormValid = commentIsValid;

  const formSubmitHandler = (event) => {
    event.preventDefault();

    if (!isFormValid) {
      return;
    }

    const commentData = {
      authTokenType: authCtx.authTokenType,
      authToken: authCtx.authToken,
      username: authCtx.userName,
      text: commentValue,
      postId: props.postId,
    };
    
    resetComment();
    sendRequest(commentData);
  }

  let hasServerError = false;
  if (requestStatus === "completed" && serverError) {
    hasServerError = true;
  }

  return (
    <>
      {hasServerError && (
        <span className={styles["error-text"]}>{serverError}</span>
      )}
      <form className={styles.newcomment} onSubmit={formSubmitHandler}>
        <Input
          type="text"
          placeholder="Add a comment"
          onChange={commentChangeHandler}
          onBlur={commentBlurHandler}
          value={commentValue}
        />
        <Button type="submit" disabled={!isFormValid}>
          Send
        </Button>
      </form>
    </>
  );
}

export default NewCommentForm;