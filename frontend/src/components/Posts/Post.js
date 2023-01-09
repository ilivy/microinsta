import { useContext, useEffect, useState } from "react";

import AuthContext from "../../store/auth-context";
import { deletePost as apiDeletePost } from "../../lib/api";
import useHttp from "../../hooks/use-http";

import Comments from "../Comments/Comments";

import Button from "../UI/Button";
import LoadingSpinner from "../UI/LoadingSpinner";

import styles from "./Post.module.css";


const BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8000/v1/"
    : "/api/v1/";

const Post = (props) => {
  const authCtx = useContext(AuthContext);
  const authCtxToken = authCtx.authTokenType + " " + authCtx.authToken;
  const userId = authCtx.userId;
  const [imageUrl, setImageUrl] = useState();

  const { image_url_type: imgUrlType, image_url: imgUrl } = props.post;

  useEffect(() => {
    if (imgUrlType === 'absolute') {
      setImageUrl(imgUrl)
    } else {
      setImageUrl(BASE_URL + imgUrl)
    }
  }, [imgUrlType, imgUrl]);

  const {
    sendRequest: sendDeletePost,
    status: deleteRequestStatus,
    error: deletePostServerError,
  } = useHttp(apiDeletePost);

  const deleteHandler = () => {
    sendDeletePost({postId: props.post.id, auth: authCtxToken});
  }

  if (deleteRequestStatus === "completed" && !deletePostServerError) {
    return <></>;
  }

  if (deleteRequestStatus === "pending") {
    return <div className="centered"><LoadingSpinner /></div>
  }

  return (
    <div className={styles.post}>
      <div className={styles["post-header"]}>
        <div className={styles["post-header-info"]}>
          <h3>{props.post.user.username}</h3>
          {+props.post.user_id === +userId && (
            <Button onClick={deleteHandler}>Delete</Button>
          )}
        </div>
      </div>

      <img src={imageUrl} alt={props.post.caption} />

      <span className={styles["post-prediction"]}>{props.post.prediction}</span>
      <h4 className={styles["post-text"]}>{props.post.caption}</h4>

      <Comments postId={props.post.id} comments={props.post.comments} />
    </div>
  );
}

export default Post;