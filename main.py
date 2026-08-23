from app.agent import TestingAgent


def print_separator(char="=", length=60):
    print(char * length)


def print_discovered_elements(elements):
    """
    Display all elements discovered by Playwright.
    """

    print("\n")
    print_separator()
    print("DISCOVERED WEB ELEMENTS")
    print_separator()

    if not elements:

        print("No elements discovered.")
        return

    print(
        f"\nTotal Elements Found: "
        f"{len(elements)}"
    )

    for index, element in enumerate(
        elements,
        start=1
    ):

        print("\n" + "-" * 60)

        print(
            f"Element #{index}"
        )

        print("-" * 60)

        print(
            f"Tag           : "
            f"{element.get('tag')}"
        )

        print(
            f"Index         : "
            f"{element.get('index')}"
        )

        print(
            f"ID            : "
            f"{element.get('id')}"
        )

        print(
            f"Name          : "
            f"{element.get('name')}"
        )

        print(
            f"Type          : "
            f"{element.get('type')}"
        )

        print(
            f"Placeholder    : "
            f"{element.get('placeholder')}"
        )

        print(
            f"ARIA Label     : "
            f"{element.get('aria_label')}"
        )

        print(
            f"Role          : "
            f"{element.get('role')}"
        )

        print(
            f"Text          : "
            f"{element.get('text')}"
        )

        print(
            f"Href          : "
            f"{element.get('href')}"
        )

        print(
            f"Title         : "
            f"{element.get('title')}"
        )

        print(
            f"Value         : "
            f"{element.get('value')}"
        )

        print(
            f"Visible       : "
            f"{element.get('visible')}"
        )

        print(
            f"Enabled       : "
            f"{element.get('enabled')}"
        )

        print(
            f"Checked       : "
            f"{element.get('checked')}"
        )

        print(
            f"CSS Selector  : "
            f"{element.get('css_selector')}"
        )

        print(
            f"XPath         : "
            f"{element.get('xpath')}"
        )

        print(
            f"Playwright    : "
            f"{element.get('playwright_locator')}"
        )

        # --------------------------------------------------
        # OPTIONS FOR SELECT
        # --------------------------------------------------

        options = element.get(
            "options"
        )

        if options:

            print(
                "\nSelect Options:"
            )

            for option in options:

                print(
                    f"   Text  : "
                    f"{option.get('text')}"
                )

                print(
                    f"   Value : "
                    f"{option.get('value')}"
                )

        # --------------------------------------------------
        # OUTER HTML
        # --------------------------------------------------

        outer_html = element.get(
            "outer_html"
        )

        if outer_html:

            print(
                "\nOuter HTML:"
            )

            print(
                outer_html
            )


def print_test_cases(test_cases):
    """
    Display generated test cases.
    """

    print("\n")
    print_separator()
    print("GENERATED TEST CASES")
    print_separator()

    if not test_cases:

        print(
            "No test cases generated."
        )

        return

    print(test_cases)


def print_playwright_code(code):
    """
    Display generated Playwright code.
    """

    print("\n")
    print_separator()
    print("GENERATED PLAYWRIGHT SCRIPT")
    print_separator()

    if not code:

        print(
            "No Playwright script generated."
        )

        return

    print(code)


def print_validation(validation):
    """
    Display Playwright validation result.
    """

    print("\n")
    print_separator()
    print("PLAYWRIGHT VALIDATION")
    print_separator()

    if not validation:

        print(
            "Validation information unavailable."
        )

        return

    valid = validation.get(
        "valid",
        False
    )

    if valid:

        print(
            "\nSTATUS: PASSED"
        )

        print(
            "Generated Playwright code "
            "passed validation."
        )

    else:

        print(
            "\nSTATUS: FAILED"
        )

        errors = validation.get(
            "errors",
            []
        )

        if errors:

            print(
                "\nValidation Errors:"
            )

            for error in errors:

                print(
                    f"  - {error}"
                )


def print_page_information(response):
    """
    Display basic page information.
    """

    print("\n")
    print_separator()
    print("PAGE INFORMATION")
    print_separator()

    print(
        f"URL   : "
        f"{response.get('url')}"
    )

    print(
        f"Title : "
        f"{response.get('title')}"
    )

    print(
        f"Status: "
        f"{response.get('status')}"
    )


def main():

    agent = TestingAgent()

    print_separator()

    print(
        "AI Software Testing Agent"
    )

    print_separator()

    print(
        "\nType 'exit' to close the agent."
    )

    while True:

        try:

            prompt = input(
                "\nYou: "
            )

        except KeyboardInterrupt:

            print(
                "\n\nExiting..."
            )

            break

        except EOFError:

            print(
                "\n\nExiting..."
            )

            break

        # --------------------------------------------------
        # Empty input
        # --------------------------------------------------

        if not prompt.strip():

            continue

        # --------------------------------------------------
        # Exit
        # --------------------------------------------------

        if prompt.strip().lower() in [
            "exit",
            "quit"
        ]:

            print(
                "\nTesting Agent stopped."
            )

            break

        # --------------------------------------------------
        # Execute Agent
        # --------------------------------------------------

        try:

            response = agent.chat(
                prompt
            )

            print("\n")
            print_separator()

            print(
                "Testing_Agent-V1"
            )

            print_separator()

            # ==================================================
            # BROWSER TESTING RESPONSE
            # ==================================================

            if isinstance(
                response,
                dict
            ):

                # ----------------------------------------------
                # Error
                # ----------------------------------------------

                if response.get(
                    "error"
                ):

                    print(
                        "\nERROR:"
                    )

                    print(
                        response.get(
                            "error"
                        )
                    )

                    continue

                # ----------------------------------------------
                # Page Information
                # ----------------------------------------------

                print_page_information(
                    response
                )

                # ----------------------------------------------
                # Discovered Elements
                # ----------------------------------------------

                print_discovered_elements(
                    response.get(
                        "elements",
                        []
                    )
                )

                # ----------------------------------------------
                # Test Cases
                # ----------------------------------------------

                print_test_cases(
                    response.get(
                        "test_cases",
                        ""
                    )
                )

                # ----------------------------------------------
                # Playwright Code
                # ----------------------------------------------

                print_playwright_code(
                    response.get(
                        "playwright_code",
                        ""
                    )
                )

                # ----------------------------------------------
                # Validation
                # ----------------------------------------------

                print_validation(
                    response.get(
                        "validation"
                    )
                )

            # ==================================================
            # NORMAL LLM RESPONSE
            # ==================================================

            else:

                print(
                    response
                )

        except Exception as e:

            print("\n")
            print_separator()

            print(
                "ERROR"
            )

            print_separator()

            print(
                str(e)
            )


if __name__ == "__main__":

    main()