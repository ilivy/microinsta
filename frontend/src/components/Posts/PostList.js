import { useEffect } from "react";

import useHttp from "../../hooks/use-http";
import { getAllPosts } from "../../lib/api";
import Post from "./Post";
import LoadingSpinner from "../UI/LoadingSpinner";

import styles from "./PostList.module.css";

const PostList = () => {
  const {
    sendRequest,
    requestStatus,
    data: loadedPosts,
    error,
  } = useHttp(getAllPosts, true);

  useEffect(() => {
    sendRequest();
  }, [sendRequest]);

  if (requestStatus === "pending") {
    return (
      <div className="centered">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return <p className="centered focused">{error}</p>;
  }

  if (requestStatus === "completed" && (!loadedPosts || loadedPosts.length === 0)) {
    return <p>No Posts found</p>;
  }

  return (
    <div className={styles.postlist}>
      {loadedPosts &&
        loadedPosts.map((post) => <Post key={post.id} post={post} />)}
    </div>
  );
}

export default PostList;