import {} from "./Button.module.css";

const Button = (props) => {
  return (
    <button onClick={props.onClick} disabled={props.disabled}>{props.children}</button>
  )
}

export default Button;