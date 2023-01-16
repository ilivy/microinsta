import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import PostList from "./PostList";

describe("Post List component", () => {

  test("renders Posts", async () => {

    window.fetch = jest.fn();
    window.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [{
        id: "11",
        user: {username: "user"},
        image_url: "image_url",
        image_url_type: "absolute",
        caption: "caption",
        prediction: "prediction came from the post",
        user_id: "12",
        comments: [{username: "username", text: "comment 1"}]
      }]
    });

    render(<PostList />);

    const postItem = await screen.findByText("prediction came from the post");
    expect(postItem).toBeInTheDocument();
  });
});
