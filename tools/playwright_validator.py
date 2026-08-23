import re


class PlaywrightValidator:

    def validate(
        self,
        code,
        url,
        page_data
    ):

        errors = []

        # ==================================================
        # BASIC CODE CHECK
        # ==================================================

        if not code:

            errors.append(
                "Generated Playwright code is empty."
            )

            return {
                "valid": False,
                "errors": errors
            }

        # ==================================================
        # URL CHECK
        # ==================================================

        if url not in code:

            errors.append(
                "Generated script does not contain "
                "the original target URL."
            )

        # ==================================================
        # FORBIDDEN URLS
        # ==================================================

        forbidden_urls = [
            "example.com",
            "google.com",
            "facebook.com",
            "youtube.com"
        ]

        for forbidden in forbidden_urls:

            if forbidden in code.lower():

                errors.append(
                    f"Generated script contains "
                    f"forbidden URL: {forbidden}"
                )

        # ==================================================
        # FORBIDDEN INVENTED SELECTORS
        # ==================================================

        forbidden_patterns = [

            "#login-button",

            "#new_password",

            'input[name="new_password"]',

            'a[href="/profile"]',

            'a[href="/settings"]',

            'a[href="https://www.google.com"]',

            "input#username",

            "input#password"
        ]

        for pattern in forbidden_patterns:

            if pattern in code:

                errors.append(
                    "Possible invented selector: "
                    + pattern
                )

        # ==================================================
        # DISCOVERED LOCATORS
        # ==================================================

        discovered_locators = set()

        for element in page_data.get(
            "elements",
            []
        ):

            locator = element.get(
                "playwright_locator"
            )

            if locator:

                discovered_locators.add(
                    locator
                )

        # ==================================================
        # IMPORTANT ELEMENT CHECK
        # ==================================================

        visible_elements = []

        for element in page_data.get(
            "elements",
            []
        ):

            if element.get(
                "visible"
            ):

                visible_elements.append(
                    element
                )

        # ==================================================
        # USERNAME CHECK
        # ==================================================

        username_found = any(
            element.get("name") == "username"
            for element in visible_elements
        )

        if username_found:

            if (
                "Username" not in code
                and 'name="username"' not in code
            ):

                errors.append(
                    "Username element was discovered "
                    "but generated script does not "
                    "appear to use it."
                )

        # ==================================================
        # PASSWORD CHECK
        # ==================================================

        password_found = any(
            element.get("name") == "password"
            for element in visible_elements
        )

        if password_found:

            if (
                "Password" not in code
                and 'name="password"' not in code
            ):

                errors.append(
                    "Password element was discovered "
                    "but generated script does not "
                    "appear to use it."
                )

        # ==================================================
        # LOGIN BUTTON CHECK
        # ==================================================

        login_button_found = any(
            (
                element.get("tag") == "button"
                and element.get("text") == "Login"
            )
            for element in visible_elements
        )

        if login_button_found:

            if (
                "name=\"Login\"" not in code
                and "name='Login'" not in code
                and "Login" not in code
            ):

                errors.append(
                    "Login button was discovered "
                    "but generated script does not "
                    "appear to use it."
                )

        # ==================================================
        # RETURN
        # ==================================================

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }