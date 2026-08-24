from models.llama_model import LlamaModel
import re


class WebTestGenerator:

    def __init__(self):

        self.model = LlamaModel()

    # ======================================================
    # FORMAT ELEMENTS
    # ======================================================

    def format_elements(
        self,
        page_data
    ):

        output = []

        for element in page_data.get(
            "elements",
            []
        ):

            # --------------------------------------------------
            # Ignore forms
            # --------------------------------------------------

            if element.get(
                "tag"
            ) == "form":

                continue

            # --------------------------------------------------
            # Ignore hidden elements
            # --------------------------------------------------

            if (
                element.get(
                    "type"
                ) == "hidden"
                or
                element.get(
                    "visible"
                ) is False
            ):

                continue

            output.append(
                {
                    "index": element.get(
                        "index"
                    ),

                    "tag": element.get(
                        "tag"
                    ),

                    "type": element.get(
                        "type"
                    ),

                    "name": element.get(
                        "name"
                    ),

                    "placeholder": element.get(
                        "placeholder"
                    ),

                    "aria_label": element.get(
                        "aria_label"
                    ),

                    "text": element.get(
                        "text"
                    ),

                    "href": element.get(
                        "href"
                    ),

                    "role": element.get(
                        "role"
                    ),

                    "css_selector": element.get(
                        "css_selector"
                    ),

                    "xpath": element.get(
                        "xpath"
                    ),

                    "playwright_locator": element.get(
                        "playwright_locator"
                    )
                }
            )

        return output

    # ======================================================
    # GENERATE TEST CASES
    # ======================================================

    def generate_test_cases(
        self,
        user_prompt,
        url,
        page_data,
        credentials
    ):

        elements = (
            self.format_elements(
                page_data
            )
        )

        username = (
            credentials.get(
                "username"
            )
        )

        password = (
            credentials.get(
                "password"
            )
        )

        # --------------------------------------------------
        # Credential information
        # --------------------------------------------------

        credential_info = ""

        if username:

            credential_info += (
                f"\nUsername: {username}"
            )

        if password:

            credential_info += (
                f"\nPassword: {password}"
            )

        prompt = f"""
You are a professional QA test engineer.

==================================================
USER TEST REQUEST
==================================================

{user_prompt}

==================================================
TARGET PAGE
==================================================

{url}

==================================================
PAGE TITLE
==================================================

{page_data.get("title")}

==================================================
TEST CREDENTIALS
==================================================

{credential_info}

These credentials were explicitly supplied by
the user for this test execution.

Use them exactly when creating the valid-login
test case.

Do not invent different credentials.

Do not store credentials in the page snapshot.

==================================================
ACTUAL UI ELEMENTS DISCOVERED BY PLAYWRIGHT
==================================================

{elements}

==================================================
IMPORTANT RULES
==================================================

The discovered elements above are the source
of truth for the webpage.

Only use UI elements that actually appear
in the discovered element list.

Do NOT invent:

- fields
- buttons
- links
- URLs
- selectors
- error messages
- dashboard
- profile
- settings
- forgot password
- password reset
- account lockout
- additional pages

Do not assume functionality that was not
observed from the page.

For the login test, use the credentials supplied
by the user.

If the user supplied credentials, include a
valid-login test case.

You may include negative login scenarios only
when appropriate.

Do not invent specific error messages.

Do not claim that a particular post-login page
exists unless it was actually observed.

==================================================
OUTPUT FORMAT
==================================================

TEST CASE ID:
TEST CASE NAME:
PRECONDITION:
STEPS:
TEST DATA:
EXPECTED RESULT:

Return plain text only.

Do not generate Python code.

Do not add explanations before or after the
test cases.
"""

        return self.model.ask(
            prompt
        )

    # ======================================================
    # GENERATE PLAYWRIGHT
    # ======================================================

    def generate_playwright(
        self,
        user_prompt,
        url,
        page_data,
        test_cases,
        credentials
    ):

        elements = (
            self.format_elements(
                page_data
            )
        )

        username = (
            credentials.get(
                "username"
            )
        )

        password = (
            credentials.get(
                "password"
            )
        )

        prompt = f"""
You are a senior Python Playwright automation engineer.

Your ONLY task is to generate an executable Python
Playwright automation script.

==================================================
USER TEST REQUEST
==================================================

{user_prompt}

==================================================
REAL TARGET URL
==================================================

{url}

==================================================
USER-PROVIDED TEST CREDENTIALS
==================================================

Username:
{username}

Password:
{password}

These credentials were explicitly provided by
the user for this test execution.

Use them exactly.

Do not invent or modify the credentials.

Do not print the password.

==================================================
STORED PAGE SNAPSHOT
==================================================

PAGE TITLE:

{page_data.get("title")}

ACTUAL DISCOVERED ELEMENTS:

{elements}

==================================================
GENERATED TEST CASES
==================================================

{test_cases}

==================================================
CRITICAL RULES
==================================================

RULE 1:
Navigate to EXACTLY this URL:

{url}

RULE 2:
Never use example.com.

RULE 3:
Never invent another URL.

RULE 4:
Never invent selectors.

RULE 5:
Use the actual Playwright locators supplied
by the stored page snapshot.

RULE 6:
A Playwright locator is a PYTHON EXPRESSION.

It is NOT a CSS selector string.

For example, if the stored page says:

page.get_by_placeholder("Username")

then the correct code is:

page.get_by_placeholder("Username").fill("{username}")

NOT:

page.fill(
    'page.get_by_placeholder("Username")',
    "{username}"
)

RULE 7:
For the password field, if the stored page says:

page.get_by_placeholder("Password")

generate:

page.get_by_placeholder("Password").fill("{password}")

NOT:

page.fill(
    'page.get_by_placeholder("Password")',
    "{password}"
)

RULE 8:
If the stored page says:

page.get_by_role("button", name="Login")

generate:

page.get_by_role(
    "button",
    name="Login"
).click()

NOT:

page.click(
    'page.get_by_role("button", name="Login")'
)

RULE 9:
Use the username exactly:

{username}

RULE 10:
Use the password exactly:

{password}

RULE 11:
Do not hard-code different credentials.

RULE 12:
Do not invent:

- profile
- settings
- dashboard
- forgot password
- password reset
- new password
- account lockout
- error messages

unless they actually exist in the stored page
specification.

RULE 13:
Do not generate generic examples.

RULE 14:
Do not use Selenium.

RULE 15:
Use Python Playwright sync API.

RULE 16:
Launch Chromium with:

headless=False

RULE 17:
Create a new browser page.

RULE 18:
Navigate to the exact target URL.

RULE 19:
Fill the actual username field.

RULE 20:
Fill the actual password field.

RULE 21:
Click the actual Login button.

RULE 22:
Wait for the login operation to complete.

RULE 23:
Print the current URL after login.

RULE 24:
Print the page title after login.

RULE 25:
Never print the password.

RULE 26:
Close the browser.

==================================================
VERY IMPORTANT OUTPUT RULE
==================================================

RETURN ONLY PYTHON CODE.

The response MUST begin with:

from playwright.sync_api import sync_playwright

The response MUST NOT contain:

- explanations
- "Here is the code"
- "Here's the solution"
- "Key points"
- summaries
- markdown
- ```python
- ```
- text before the Python program
- text after the Python program

The response will be saved directly to a .py
file and executed by Python.

Therefore it MUST be valid Python syntax.

The response MUST end with executable Python code.

==================================================
EXPECTED STRUCTURE
==================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(
        "{url}"
    )

    # actual username locator

    # actual password locator

    # actual login locator

    # wait for result

    print(page.url)
    print(page.title())

    browser.close()

Generate ONLY the executable Python program.
"""

        response = self.model.ask(
            prompt
        )

        return self.clean_code(
            response
        )

    # ======================================================
    # CLEAN QWEN RESPONSE
    # ======================================================

    def clean_code(
        self,
        code
    ):

        if not code:

            return ""

        code = code.strip()

        # ==================================================
        # REMOVE MARKDOWN FENCES
        # ==================================================

        code = code.replace(
            "```python",
            ""
        )

        code = code.replace(
            "```py",
            ""
        )

        code = code.replace(
            "```",
            ""
        )

        code = code.strip()

        # ==================================================
        # FIND PYTHON START
        # ==================================================

        markers = [
            "from playwright.sync_api import sync_playwright",
            "import playwright"
        ]

        positions = []

        for marker in markers:

            position = code.find(
                marker
            )

            if position >= 0:

                positions.append(
                    position
                )

        if positions:

            code = code[
                min(positions):
            ]

        # ==================================================
        # REMOVE TEXT AFTER browser.close()
        #
        # This fixes the exact error from your run.
        # ==================================================

        browser_close_positions = [

            code.find(
                "browser.close()"
            ),

            code.find(
                "browser.close ()"
            )
        ]

        browser_close_positions = [
            position
            for position in browser_close_positions
            if position >= 0
        ]

        if browser_close_positions:

            end_position = (
                min(
                    browser_close_positions
                )
                + len(
                    "browser.close()"
                )
            )

            code = code[
                :end_position
            ]

        # ==================================================
        # FIX COMMON QWEN LOCATOR ERRORS
        # ==================================================

        # --------------------------------------------------
        # WRONG:
        #
        # page.fill(
        #     'page.get_by_placeholder("Username")',
        #     "ADMIN"
        # )
        #
        # CORRECT:
        #
        # page.get_by_placeholder("Username").fill("Admin")
        # --------------------------------------------------

        pattern = (
            r'''page\.fill\(\s*'''
            r'''['"]page\.get_by_placeholder\("'''
            r'''([^"]+)'''
            r'''"\)['"]\s*,\s*'''
            r'''(["'].*?["'])'''
            r'''\s*\)'''
        )

        code = re.sub(
            pattern,
            r'page.get_by_placeholder("\1").fill(\2)',
            code
        )

        # ==================================================
        # FIX SINGLE-LINE LOCATOR FILL
        # ==================================================

        pattern = (
            r'''page\.fill\(\s*'''
            r'''['"]page\.get_by_placeholder\('''
            r'''["']([^"']+)["']'''
            r'''\)['"]\s*,\s*'''
            r'''(["'].*?["'])'''
            r'''\s*\)'''
        )

        code = re.sub(
            pattern,
            r'page.get_by_placeholder("\1").fill(\2)',
            code
        )

        # ==================================================
        # FIX WRONG LOGIN CLICK
        # ==================================================

        pattern = (
            r'''page\.click\(\s*'''
            r'''['"]page\.get_by_role\("button",'''
            r'''\s*name="([^"]+)"\)['"]'''
            r'''\s*\)'''
        )

        code = re.sub(
            pattern,
            r'page.get_by_role("button", name="\1").click()',
            code
        )

        # ==================================================
        # FIX SINGLE-QUOTE ROLE LOCATOR
        # ==================================================

        pattern = (
            r'''page\.click\(\s*'''
            r'''["']page\.get_by_role\('button','''
            r'''\s*name=['"]([^'"]+)['"]'''
            r'''\)['"]\s*\)'''
        )

        code = re.sub(
            pattern,
            r'page.get_by_role("button", name="\1").click()',
            code
        )

        # ==================================================
        # REMOVE OBVIOUS NON-PYTHON LINES
        # ==================================================

        lines = code.splitlines()

        cleaned_lines = []

        for line in lines:

            stripped = line.strip()

            # Ignore common Qwen explanations
            if stripped.startswith(
                "**Key points"
            ):

                break

            if stripped.startswith(
                "### Key points"
            ):

                break

            if stripped.startswith(
                "Key points:"
            ):

                break

            if stripped.startswith(
                "This script"
            ):

                break

            if stripped.startswith(
                "This code"
            ):

                break

            cleaned_lines.append(
                line
            )

        code = "\n".join(
            cleaned_lines
        )

        return code.strip()