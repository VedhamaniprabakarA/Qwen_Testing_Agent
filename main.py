from app.agent import TestingAgent


def print_separator(
    char="=",
    length=60
):

    print(
        char * length
    )


def print_discovered_elements(
    elements
):

    print("\n")
    print_separator()

    print(
        "DISCOVERED WEB ELEMENTS"
    )

    print_separator()

    if not elements:

        print(
            "No elements discovered."
        )

        return

    print(
        f"\nTotal Elements Found: "
        f"{len(elements)}"
    )

    for index, element in enumerate(
        elements,
        start=1
    ):

        print(
            "\n" + "-" * 60
        )

        print(
            f"Element #{index}"
        )

        print("-" * 60)

        print(
            f"Tag           : "
            f"{element.get('tag')}"
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
            f"Visible       : "
            f"{element.get('visible')}"
        )

        print(
            f"Enabled       : "
            f"{element.get('enabled')}"
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


def print_test_cases(
    test_cases
):

    print("\n")
    print_separator()

    print(
        "GENERATED TEST CASES"
    )

    print_separator()

    if not test_cases:

        print(
            "No test cases generated."
        )

        return

    print(
        test_cases
    )


def print_playwright_code(
    code
):

    print("\n")
    print_separator()

    print(
        "GENERATED PLAYWRIGHT SCRIPT"
    )

    print_separator()

    if not code:

        print(
            "No Playwright script generated."
        )

        return

    print(
        code
    )


def print_execution_result(
    execution
):

    print("\n")
    print_separator()

    print(
        "AUTOMATION EXECUTION RESULT"
    )

    print_separator()

    if not execution:

        print(
            "No execution information."
        )

        return

    print(
        f"Status       : "
        f"{execution.get('status')}"
    )

    print(
        f"Return Code  : "
        f"{execution.get('return_code')}"
    )

    if execution.get(
        "script_path"
    ):

        print(
            f"Script       : "
            f"{execution.get('script_path')}"
        )

    # --------------------------------------------------
    # Standard output
    # --------------------------------------------------

    stdout = execution.get(
        "stdout"
    )

    if stdout:

        print("\n")
        print(
            "PLAYWRIGHT OUTPUT"
        )

        print("-" * 60)

        print(
            stdout
        )

    # --------------------------------------------------
    # Error output
    # --------------------------------------------------

    stderr = execution.get(
        "stderr"
    )

    if stderr:

        print("\n")
        print(
            "PLAYWRIGHT ERROR"
        )

        print("-" * 60)

        print(
            stderr
        )


def print_page_information(
    response
):

    print("\n")
    print_separator()

    print(
        "PAGE INFORMATION"
    )

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

        # ==================================================
        # EMPTY INPUT
        # ==================================================

        if not prompt.strip():

            continue

        # ==================================================
        # EXIT
        # ==================================================

        if prompt.strip().lower() in [
            "exit",
            "quit"
        ]:

            print(
                "\nTesting Agent stopped."
            )

            break

        # ==================================================
        # EXECUTE AGENT
        # ==================================================

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
            # BROWSER TEST RESPONSE
            # ==================================================

            if isinstance(
                response,
                dict
            ):

                # --------------------------------------------------
                # ERROR
                # --------------------------------------------------

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

                # --------------------------------------------------
                # PAGE
                # --------------------------------------------------

                print_page_information(
                    response
                )

                # --------------------------------------------------
                # ELEMENTS
                # --------------------------------------------------

                print_discovered_elements(
                    response.get(
                        "elements",
                        []
                    )
                )

                # --------------------------------------------------
                # TEST CASES
                # --------------------------------------------------

                print_test_cases(
                    response.get(
                        "test_cases",
                        ""
                    )
                )

                # --------------------------------------------------
                # PLAYWRIGHT
                # --------------------------------------------------

                print_playwright_code(
                    response.get(
                        "playwright_code",
                        ""
                    )
                )

                # --------------------------------------------------
                # EXECUTION
                # --------------------------------------------------

                print_execution_result(
                    response.get(
                        "execution",
                        {}
                    )
                )

                # --------------------------------------------------
                # SNAPSHOT
                # --------------------------------------------------

                print("\n")
                print_separator()

                print(
                    "PAGE SNAPSHOT"
                )

                print_separator()

                print(
                    response.get(
                        "snapshot"
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