import { useCallback, useContext } from "react";

import AuthContext from "../../store/auth-context";
import { getPostComments } from "../../lib/api";
import useHttp from "../../hooks/use-http";

import LoadingSpinner from "../UI/LoadingSpinner";
import CommentItem from "./CommentItem";
import NewCommentForm from "./NewCommentForm";

import styles from "./Comments.module.css";

const Comments = (props) => {
  const authCtx = useContext(AuthContext);

  const {
    sendRequest,
    status: requestStatus,
    data: loadedComments,
  } = useHttp(getPostComments);

  const addedCommentHandler = useCallback(() => {
    sendRequest(props.postId);
  }, [sendRequest, props.postId]);

  let comments = props.comments;
  if (loadedComments) {
    comments = loadedComments;
  }

  if (requestStatus === "pending") {
    return <div className="centered"><LoadingSpinner /></div>
  }

  return (
    <>
      <div className={styles.comments}>
        {comments.map((comment, idx) => (
          <CommentItem
            key={idx}
            text={comment.text}
            username={comment.username}
          />
        ))}
      </div>
      {authCtx.isLoggedIn && (
        <NewCommentForm
          postId={props.postId}
          onAddedComment={addedCommentHandler}
        />
      )}
    </>
  );
}

export default Comments;