import { useContext } from "react";

import AuthContext from "../../store/auth-context";
import ImageUpload from "../Posts/ImageUpload";
import {} from "./MainFooter.module.css";

const MainFooter = () => {
  const authCtx = useContext(AuthContext);
  return (
    <footer>
      {authCtx.isLoggedIn && <ImageUpload />}
    </footer>
  );
}

export default MainFooter;