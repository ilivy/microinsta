import React, { useCallback, useEffect, useState } from "react";

let logoutTimer;

const AuthContext = React.createContext({
  authToken: null,
  authTokenType: null,
  userId: null,
  userName: null,
  email: null,
  isLoggedIn: false,
  login: (authData) => {},
  signup: (authData) => {},
  logout: () => {},
});

const calculateRemainingTime = (expirationTime) => {
  /**
   * Calculates for how long the authentication token is valid
   * (in milliseconds)
   */
  const currentTime = new Date().getTime();
  const adjExpirationTime = new Date(expirationTime).getTime();

  const remainingTime = adjExpirationTime - currentTime;

  return remainingTime;
};

const retrieveStoredToken = () => {
  /**
   * gets the authentication token from the localStorage
   * 
   * if the token is expired in 1 minute
   * removes auth data from the localStorage
   */
  const storedToken = localStorage.getItem("authToken");
  const storedExpirationDate = localStorage.getItem("expirationTime");

  const remainingTime = calculateRemainingTime(storedExpirationDate);

  if (remainingTime <= 60000) {
    localStorage.removeItem("authToken");
    localStorage.removeItem("expirationTime");
    return null;
  }

  return {
    token: storedToken,
    duration: remainingTime,
  }
};

export const AuthContextProvider = (props) => {
  /**
   * tokenData is used here to watch the expiration time
   */
  const tokenData = retrieveStoredToken();

  const [authToken, setAuthToken] = useState(localStorage.getItem("authToken"));
  const [authTokenType, setAuthTokenType] = useState(localStorage.getItem("authTokenType"));
  const [userId, setUserId] = useState(localStorage.getItem("userId"));
  const [userName, setUserName] = useState(localStorage.getItem("userName"));
  const [email, setEmail] = useState(localStorage.getItem("email"));

  const isLoggedIn = !!authToken;

  const logoutHandler = useCallback(() => {
    setAuthToken(null);
    localStorage.removeItem("authToken");
    
    setAuthTokenType(null);
    localStorage.removeItem("authTokenType");

    setUserId(null);
    localStorage.removeItem("userId");

    setUserName(null);
    localStorage.removeItem("userName");

    setEmail(null);
    localStorage.removeItem("email");
  }, []);

  useEffect(() => {
    if (logoutTimer) {
      clearTimeout(logoutTimer); 
    }

    if (tokenData) {
      logoutTimer = setTimeout(logoutHandler, tokenData.duration);
    }
  }, [tokenData, logoutHandler]);

  const loginHandler = (authData) => {
    setAuthToken(authData["access_token"]);
    localStorage.setItem("authToken", authData["access_token"]);
    
    setAuthTokenType(authData["token_type"]);
    localStorage.setItem("authTokenType", authData["token_type"]);

    setUserId(authData["user_id"]);
    localStorage.setItem("userId", authData["user_id"]);

    setUserName(authData["username"]);
    localStorage.setItem("userName", authData["username"]);

    setEmail(authData["email"]);
    localStorage.setItem("email", authData["email"]);

    /**
     * Auth data will be expired in 2 hours
     */
    const expirationTime = new Date(
      new Date().getTime() + 2 * 60 * 60 * 1000
    ).toISOString();

    localStorage.setItem("expirationTime", expirationTime);

    const remainingTime = calculateRemainingTime(expirationTime);

    logoutTimer = setTimeout(logoutHandler, remainingTime);
  };

  const signupHandler = (authData) => {
    setUserId(authData["id"]);
    localStorage.setItem("userId", authData["id"]);

    setUserName(authData["username"]);
    localStorage.setItem("userName", authData["username"]);

    setEmail(authData["email"]);
    localStorage.setItem("email", authData["email"]);
  };

  const contextValue = {
    authToken,
    authTokenType,
    userId,
    userName,
    email,
    isLoggedIn,
    login: loginHandler,
    signup: signupHandler,
    logout: logoutHandler,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {props.children}
    </AuthContext.Provider>
  );
}

export default AuthContext;