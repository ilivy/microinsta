import { useContext } from "react";

import Button from "../UI/Button";
import logoImg from "../../assets/logo.png";
import AuthContext from "../../store/auth-context";
import styles from "./MainNavigation.module.css";

const MainNavigation = (props) => {
  const authCtx = useContext(AuthContext);

  const logoutHandler = () => {
    authCtx.logout();
  }

  return (
    <header className={styles.header}>
      <img src={logoImg} className={styles.logo} alt="Logo Micro Insta" />
      <nav>
        <ul>
          {!authCtx.isLoggedIn && <li><Button onClick={props.onShowLogin}>Login</Button></li>}
          {!authCtx.isLoggedIn && <li><Button onClick={props.onShowSignUp}>Sign up</Button></li>}
          {authCtx.isLoggedIn && <li>Hey, {authCtx.userName}!</li>}
          {authCtx.isLoggedIn && <li><Button onClick={logoutHandler}>Logout</Button></li>}
        </ul>
      </nav>
    </header>
  );
};

export default MainNavigation;
