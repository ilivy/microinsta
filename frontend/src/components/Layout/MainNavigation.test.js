import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import MainNavigation from "./MainNavigation";

describe("Main Navigation component", () => {

  test("renders Login button", () => {
    render(<MainNavigation />);

    const loginTxt = screen.getByText("Login");
    expect(loginTxt).toBeInTheDocument();
  });
});
