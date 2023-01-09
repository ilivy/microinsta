import { useContext, useEffect, useState } from "react";

import Input from "../UI/Input";
import Button from "../UI/Button";
import LoadingSpinner from "../UI/LoadingSpinner";

import AuthContext from "../../store/auth-context";
import { createPost as apiCreatePost, uploadImage as apiUploadImage } from "../../lib/api";
import useHttp from "../../hooks/use-http";

import styles from "./ImageUpload.module.css";

const ImageUpload = () => {
  const authCtx = useContext(AuthContext);
  const authCtxToken = authCtx.authTokenType + " " + authCtx.authToken;
  const userId = authCtx.userId;

  const [caption, setCaption] = useState("");
  const [image, setImage] = useState(null);

  const {
    sendRequest: sendImage,
    status: imgRequestStatus,
    data: imgServerResponseData,
    error: imgServerError,
  } = useHttp(apiUploadImage);

  const {
    sendRequest: sendNewPost,
    status: postRequestStatus,
    error: postServerError,
  } = useHttp(apiCreatePost);

  const captionInputHandler = (event) => {
    setCaption(event.target.value);
  }

  const fileInputHandler = (event) => {
    if (event.target.files[0]) {
      setImage(event.target.files[0])
    }
  }

  const uploadHandler = (event) => {
    event.preventDefault();

    if (image) {
      sendImage({image: image, auth: authCtxToken});
    }
  }

  useEffect(() => {
    if (imgRequestStatus === "completed" && !imgServerError) {
      const postData = {
        url: imgServerResponseData.filename,
        prediction: imgServerResponseData.photo_prediction,
        caption,
        userId,
      }

      sendNewPost({post: postData, auth: authCtxToken});
    }
  }, [
    imgRequestStatus,
    imgServerError,
    imgServerResponseData,
    sendNewPost,
    authCtxToken,
    userId,
    caption,
  ]);

  useEffect(() => {
    if (postRequestStatus === "completed" && !postServerError) {
      window.location.reload();
    }
  }, [postRequestStatus, postServerError]);

  if (imgRequestStatus === "pending" || postRequestStatus === "pending" ) {
    return <div className="centered"><LoadingSpinner /></div>
  }

  return (
    <div className={styles.upload}>
      <Input
        type="text"
        placeholder="Enter a caption"
        onChange={captionInputHandler}
        value={caption}
      />
      <input
        type="file"
        id="file-input"
        onChange={fileInputHandler}
      />
      <Button onClick={uploadHandler}>Upload</Button>
    </div>
  );
}

export default ImageUpload;