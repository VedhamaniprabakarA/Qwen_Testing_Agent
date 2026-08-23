from models.llama_model import LlamaModel


class WebTestGenerator:

    def __init__(self):

        self.model = LlamaModel()

    # ==========================================================
    # FORMAT ELEMENTS FOR QWEN
    # ==========================================================

    def format_elements(self, page_data):

        output = []

        for element in page_data.get(
            "elements",
            []
        ):

            # Ignore forms for normal UI generation
            if element.get("tag") == "form":
                continue

            # Ignore hidden inputs
            if (
                element.get("type") == "hidden"
                or element.get("visible") is False
            ):
                continue

            output.append(
                {
                    "index": element.get("index"),
                    "tag": element.get("tag"),
                    "type": element.get("type"),
                    "name": element.get("name"),
                    "placeholder": element.get(
                        "placeholder"
                    ),
                    "text": element.get("text"),
                    "href": element.get("href"),
                    "role": element.get("role"),
                    "css_selector": element.get(
                        "css_selector"
                    ),
                    "xpath": element.get("xpath"),
                    "playwright_locator": element.get(
                        "playwright_locator"
                    )
                }
            )

        return output

    # ==========================================================
    # GENERATE TEST CASES
    # ==========================================================

    def generate_test_cases(
        self,
        url,
        page_data
    ):

        elements = self.format_elements(
            page_data
        )

        prompt = f"""
You are a professional QA test engineer.

TARGET PAGE:
{url}

PAGE TITLE:
{page_data.get("title")}

ACTUAL UI ELEMENTS DISCOVERED BY PLAYWRIGHT:
{elements}

Your task is to generate functional test cases.

IMPORTANT:

Only use UI elements that appear in the
ACTUAL UI ELEMENTS list.

Do NOT invent:

- error messages
- dashboard
- profile page
- settings page
- forgot password
- password change
- additional fields
- additional buttons
- additional links
- additional URLs
- additional selectors

Do not assume functionality that is not visible
from the discovered page.

For this page, generate realistic test scenarios
based ONLY on the discovered elements.

For a login form, cover:

1. Valid login
2. Invalid login
3. Empty username
4. Empty password
5. Empty username and password
6. Login button behavior

Only generate link navigation tests for links that
actually appear in the discovered elements.

Do not invent expected error messages.

Return plain text test cases.

Use this format:

TEST CASE ID:
TEST CASE NAME:
PRECONDITION:
STEPS:
TEST DATA:
EXPECTED RESULT:

Do not include Python code.
"""

        return self.model.ask(
            prompt
        )

    # ==========================================================
    # GENERATE PLAYWRIGHT
    # ==========================================================

    def generate_playwright(
        self,
        url,
        page_data,
        test_cases
    ):

        elements = self.format_elements(
            page_data
        )

        prompt = f"""
You are a Python Playwright automation engineer.

Generate Playwright automation for the REAL page below.

REAL TARGET URL:

{url}

REAL DISCOVERED ELEMENTS:

{elements}

TEST CASES:

{test_cases}

==================================================
ABSOLUTE RULES
==================================================

RULE 1:
The browser MUST navigate to exactly:

{url}

RULE 2:
Never use example.com.

RULE 3:
Never use another URL.

RULE 4:
Never invent a selector.

RULE 5:
Only use selectors from the discovered elements.

RULE 6:
Use the exact Playwright locator supplied
by the discovered element whenever possible.

RULE 7:
For username use the discovered username locator.

RULE 8:
For password use the discovered password locator.

RULE 9:
For Login use the discovered Login button locator.

RULE 10:
Do not invent:

profile
settings
dashboard
Google
Facebook
Twitter
LinkedIn
new_password
error-message

unless the corresponding element exists
in the discovered element list.

RULE 11:
Do not create fake test cases.

RULE 12:
Do not create generic Playwright examples.

RULE 13:
Do not use example.com.

RULE 14:
Do not explain the code.

RULE 15:
Return ONLY Python code.

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

    # actual discovered elements

    browser.close()

Generate the final executable Python script now.
"""

        response = self.model.ask(
            prompt
        )

        return self.clean_code(
            response
        )

    # ==========================================================
    # CLEAN QWEN MARKDOWN
    # ==========================================================

    def clean_code(
        self,
        code
    ):

        if not code:
            return ""

        code = code.strip()

        if "```python" in code:

            code = code.replace(
                "```python",
                ""
            )

        if "```" in code:

            code = code.replace(
                "```",
                ""
            )

        return code.strip()