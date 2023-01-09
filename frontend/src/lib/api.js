const BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8000/v1/"
    : "/api/v1/";

export async function getAllPosts() {
  const response = await fetch(BASE_URL + "posts/all");
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || "Could not fetch posts.");
  }

  const posts = data.sort((a, b) => {
    const t_a = a.created_at.split(/[-T:]/);
    const t_b = b.created_at.split(/[-T:]/);
    const d_a = new Date(
      Date.UTC(t_a[0], t_a[1] - 1, t_a[2], t_a[3], t_a[4], t_a[5])
    );
    const d_b = new Date(
      Date.UTC(t_b[0], t_b[1] - 1, t_b[2], t_b[3], t_b[4], t_b[5])
    );
    return d_b - d_a;
  });

  return posts;
}

export async function getPostComments(postId) {
  const response = await fetch(BASE_URL + "comments/all/" + postId);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || 'Could not fetch comments.');
  }

  return data;
}

export async function login(loginData) {
  const requestData = {
    method: "POST",
    body: loginData,
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
  };

  const response = await fetch(BASE_URL + "login", requestData);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not login.");
  }

  return data;
}

export async function signup(userData) {
  const requestData = {
    method: "POST",
    body: userData,
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
  };

  const response = await fetch(BASE_URL + "register", requestData);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not sign up.");
  }

  return data;
}

export async function addComment(commentData) {

  const commentPayload = JSON.stringify({
    username: commentData.username,
    text: commentData.text,
    post_id: commentData.postId,
  });

  const requestData = {
    method: "POST",
    body: commentPayload,
    headers: new Headers({
      Authorization: commentData.authTokenType + " " + commentData.authToken,
      "Content-Type": "application/json",
    }),
  };

  const response = await fetch(BASE_URL + "comments", requestData);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not add a comment.");
  }

  return data;
}

export async function uploadImage(imageData) {

  const formData = new FormData();
  formData.append("image", imageData.image);

  const requestData = {
    method: "POST",
    headers: new Headers({
      Authorization: imageData.auth,
    }),
    body: formData,
  };

  const response = await fetch(BASE_URL + "posts/image", requestData);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not upload an image.");
  }

  return data;
}

export async function createPost(postData) {

  const imageData = postData.post;
  const authData = postData.auth;

  const jsonString = JSON.stringify({
    image_url: imageData.url,
    image_url_type: "absolute",
    prediction: imageData.prediction,
    caption: imageData.caption,
    user_id: imageData.userId,
  });

  const requestData = {
    method: "POST",
    headers: new Headers({
      Authorization: authData,
      "Content-Type": "application/json",
    }),
    body: jsonString,
  };

  const response = await fetch(BASE_URL + "posts", requestData);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Could not create a Post.");
  }

  return data;
}

export async function deletePost(postData) {

  const requestData = {
    method: "DELETE",
    headers: new Headers({
      Authorization: postData.auth,
    }),
  };

  const response = await fetch(BASE_URL + "posts/delete/" + postData.postId, requestData);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || 'Could not delete Post.');
  }

  return data;
}
