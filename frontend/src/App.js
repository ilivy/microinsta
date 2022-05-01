import React, {useState, useEffect} from 'react';
import {Button, Modal, Input} from "@mui/material";
import './App.css';
import Post from './Post';
import ImageUpload from './ImageUpload';

const BASE_URL =
  process.env.NODE_ENV === 'development'
   ? 'http://localhost:8000/v1/'
   : '/api/v1/';

function App() {
    
  const [posts, setPosts] = useState([]);
  const [openSignIn, setOpenSignIn] = useState(false);
  const [openSignUp, setOpenSignUp] = useState(false);
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [authToken, setAuthToken] = useState(null);
  const [authTokenType, setAuthTokenType] = useState(null);
  const [userId, setUserId] = useState('');

  useEffect(() => {
    setAuthToken(window.localStorage.getItem('authToken'));
    setAuthTokenType(window.localStorage.getItem('authTokenType'));
    setUserId(window.localStorage.getItem('userId'));
    setUsername(window.localStorage.getItem('username'));
    setEmail(window.localStorage.getItem('email'));
  }, [])

  useEffect(() => {
    authToken
      ? window.localStorage.setItem('authToken', authToken)
      : window.localStorage.removeItem('authToken')
    authTokenType
      ? window.localStorage.setItem('authTokenType', authTokenType)
      : window.localStorage.removeItem('authTokenType')
    userId
      ? window.localStorage.setItem('userId', userId)
      : window.localStorage.removeItem('userId')
    username
      ? window.localStorage.setItem('username', username)
      : window.localStorage.removeItem('username')
    email
      ? window.localStorage.setItem('email', email)
      : window.localStorage.removeItem('email')
  }, [authToken, authTokenType, userId, username, email])
  
  useEffect(() => {
    fetch(BASE_URL + 'posts/all')
      .then(response => {
        const res_json = response.json()
        if (response.ok) {
          return res_json
        }
        throw response
      })
      .then(data => {
        const result = data.sort((a, b) => {
          const t_a = a.created_at.split(/[-T:]/)
          const t_b = b.created_at.split(/[-T:]/)
          const d_a = new Date(Date.UTC(t_a[0], t_a[1]-1, t_a[2], t_a[3], t_a[4], t_a[5]))
          const d_b = new Date(Date.UTC(t_b[0], t_b[1]-1, t_b[2], t_b[3], t_b[4], t_b[5]))
          return d_b - d_a
        })
        return result
      })
      .then(data => {
        setPosts(data)
      })
      .catch(error => {
        console.log(error)
        alert(error)
      })
  }, [])
  
  const signUp = (event) => {
    event?.preventDefault();
    
    const json_data = JSON.stringify({
      username: username,
      email: email,
      password: password
    })
    
    const requestOptions = {
      method: 'POST',
      body: json_data,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    }
    
    fetch(BASE_URL + 'register/', requestOptions)
      .then(response => {
        if (response.ok) {
          return response.json()
        }
        throw response
      })
      .then(data => {
        signIn()
      })
      .catch(error => {
        console.log(error)
        alert(error)
      })
      
    setOpenSignUp(false);
  }
  
  const signIn = (event) => {
    event?.preventDefault();
    
    const json_data = JSON.stringify({
      email: email,
      password: password
    })
    
    const requestOptions = {
      method: 'POST',
      body: json_data,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    }
    
    fetch(BASE_URL + 'login', requestOptions)
      .then(response => {
        if (response.ok) {
          return response.json()
        }
        throw response
      })
      .then(data => {
        setAuthToken(data.access_token)
        setAuthTokenType(data.token_type)
        setUserId(data.user_id)
        setUsername(data.username)
        setEmail(data.email)
      })
      .catch(error => {
        console.log(error)
        alert(error)
      })
      
    setOpenSignIn(false);
  }
  
  const signOut = (event) => {
    setAuthToken(null)
    setAuthTokenType(null)
    setUserId('')
    setUsername('')
    setEmail('')
  }
    
  return (
    <div className="app">
        
      <Modal
        open={openSignIn}
        onClose={() => setOpenSignIn(false)}>

        <div className="signin_modal">
          <form className="app_signin">
            <center>
              <img className="app_header_image"
                src="logo192.png"
                alt="Insta" />
            </center>
            <center>
              <Input
                placeholder="email"
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)} />
            </center>
            <center>
              <Input
                placeholder="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)} />
            </center>
            <center>
              <Button
                type="submit"
                onClick={signIn}>Login</Button>
            </center>
          </form>
        </div>
      </Modal>
      
      <Modal
        open={openSignUp}
        onClose={() => setOpenSignUp(false)}>

        <div className="signin_modal">
          <form className="app_signin">
            <center>
              <img className="app_header_image"
                src="logo192.png"
                alt="Insta" />
            </center>
            <center>
              <Input
                placeholder="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)} />
            </center>
            <center>
              <Input
                placeholder="email"
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)} />
            </center>
            <center>
              <Input
                placeholder="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)} />
            </center>
            <center>
              <Button
                type="submit"
                onClick={signUp}>Sign Up</Button>
            </center>
          </form>
        </div>
      </Modal>
        
      <div className="app_header">
        <img className="app_header_image"
          src="logo192.png"
          alt="Insta" />
          
        {authToken ? (
          <span>
            <span className="app_header_username">Hey, {username}!</span>
            <Button onClick={() => signOut()}>Logout</Button>
          </span>
        ) : (
          <div>
            <Button onClick={() => setOpenSignIn(true)}>Login</Button>
            <Button onClick={() => setOpenSignUp(true)}>Sign up</Button>
          </div>
        )}
        
      </div>
      
      <div className="app_posts">
        {
          posts.map(post => (
            <Post
              key={post.id}
              post={post}
              authToken={authToken}
              authTokenType={authTokenType}
              username={username}
              userId={userId}
            />
          ))
        }
      </div>
              
      {
        authToken ? (
          <ImageUpload
            authToken={authToken}
            authTokenType={authTokenType}
            userId={userId}
          />
        ) : (
          <h3>You need to log in to make a post</h3>
        )
      }
              
    </div>
  );
}

export default App;
