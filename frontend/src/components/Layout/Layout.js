import { useState } from "react";

import LoginModal from "../Auth/LoginModal";
import SignUpModal from "../Auth/SignUpModal";
import MainNavigation from "./MainNavigation";
import MainFooter from "./MainFooter";

import styles from "./Layout.module.css";

const Layout = (props) => {
  const [isLoginShown, setIsLoginShown] = useState(false);
  const [isSignUpShown, setIsSignUpShown] = useState(false);

  const showLoginHandler = () => {
    setIsLoginShown(true);
  };

  const showSignUpHandler = () => {
    setIsSignUpShown(true);
  };

  const hideLoginHandler = () => {
    setIsLoginShown(false);
  };

  const hideSignUpHandler = () => {
    setIsSignUpShown(false);
  };

  return (
    <>
      {isLoginShown && <LoginModal onClose={hideLoginHandler} />}
      {isSignUpShown && <SignUpModal onClose={hideSignUpHandler} />}
      <div className={styles.container}>
        <MainNavigation onShowLogin={showLoginHandler} onShowSignUp={showSignUpHandler} />
        <main>{props.children}</main>
        <MainFooter />
      </div>
    </>
  );
};

export default Layout;
