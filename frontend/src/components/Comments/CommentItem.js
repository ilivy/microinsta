import styles from "./CommentItem.module.css";

const CommentItem = (props) => {
  return (
    <p>
      <strong>{props.username}:</strong> {props.text}
    </p>
  )
}

export default CommentItem;