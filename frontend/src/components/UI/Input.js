import styles from "./Input.module.css";

const Input = (props) => {
  const {hasError, ...inputProps} = props;

  return (
    <div className={`${styles.input} ${props.hasError ? styles.invalid: ""}`}>
      <input {...inputProps} />
    </div>
  );
};

export default Input;
