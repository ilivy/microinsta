import React, {useState, useEffect} from 'react';
import './Post.css';
import {Avatar, Button} from "@mui/material";

const BASE_URL =
  process.env.NODE_ENV === 'development'
   ? 'http://localhost:8000/v1/'
   : '/api/v1/';

function Post({post, authToken, authTokenType, username, userId}) {
    
  const [imageUrl, setImageUrl] = useState('');
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  
  useEffect(() => {
    if (post.image_url_type == 'absolute') {
      setImageUrl(post.image_url)
    } else {
      setImageUrl(BASE_URL + post.image_url)
    }
  }, [])
  
  useEffect(() => {
    setComments(post.comments)
  }, [])
  
  const handleDelete = (e) => {
    e?.preventDefault();
    
    const requestOptions = {
      method: 'DELETE',
      headers: new Headers({
        'Authorization': authTokenType + ' ' + authToken
      })
    }
    
    fetch(BASE_URL + 'posts/delete/' + post.id, requestOptions)
      .then(response => {
        if (response.ok) {
          window.location.reload()
        }
        throw response
      })
      .catch(error => {
        console.log(error)
      })
  }
  
  const postComment = (e) => {
    e?.preventDefault();
    
    const json_string = JSON.stringify({
      'username': username,
      'text': newComment,
      'post_id': post.id
    })
    
    const requestOptions = {
      method: 'POST',
      headers: new Headers({
        'Authorization': authTokenType + ' ' + authToken,
        'Content-Type': 'application/json'
      }),
      body: json_string
    }
    
    fetch(BASE_URL + 'comments', requestOptions)
    .then(response => {
      if (response.ok) {
        return response.json
      }
    })
    .then(data => {
      fetchComments()
    })
    .catch(error => {
      console.log(error)
    })
    .finally(() => {
      setNewComment('')
    })
  }
  
  const fetchComments = () => {
    fetch(BASE_URL + 'comments/all/' + post.id)
      .then(response => {
        if (response.ok) {
          return response.json()
        }
        throw response
      })
      .then(data => {
        setComments(data)
      })
      .catch(error => {
        console.log(error)
      })
  }
    
  return  (
    <div className="post">
        
      <div className="post_header">
        <Avatar
          alt=""
          src=""/>
          <div className="post_header_info">
            <h3>{post.user.username}</h3>
            {
              post.user_id == userId && (
                <Button className="post_delete" onClick={handleDelete}>
                  Delete
                </Button>
              )
            }
          </div>
      </div>
        
      <img
        className="post_image"
        src={imageUrl}
      />
              
      <span className="post_prediction">{post.prediction}</span>
      <h4 className="post_text">{post.caption}</h4>

        <div className="post_comments">
          {
            comments.map((comment) => (
              <p key={comment.id}>
                <strong>{comment.username}:</strong> {comment.text}
              </p>
            ))
          }
        </div>
                
        {authToken && (
          <form className="post_comment_box">
            <input
              className="post_input"
              type="text"
              placeholder="Add a comment"
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
            />
            <button
              className="post_button"
              type="submit"
              disable={!newComment}
              onClick={postComment}>
                Send
            </button>
          </form>
        )}
    </div>
  )
}

export default Post;