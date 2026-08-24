import re

from tools.browser_inspector import BrowserInspector
from tools.web_test_generator import WebTestGenerator
from tools.page_store import PageStore
from tools.playwright_executor import PlaywrightExecutor


class BrowserWorkflow:

    def __init__(self):

        # ==================================================
        # BROWSER INSPECTOR
        # ==================================================

        self.inspector = BrowserInspector(
            headless=False
        )

        # ==================================================
        # AI TEST GENERATOR
        # ==================================================

        self.generator = WebTestGenerator()

        # ==================================================
        # PAGE STORAGE
        # ==================================================

        self.page_store = PageStore()

        # ==================================================
        # PLAYWRIGHT EXECUTOR
        # ==================================================

        self.executor = PlaywrightExecutor(
            timeout=120
        )

    # ======================================================
    # MAIN WORKFLOW
    # ======================================================

    def execute(
        self,
        user_prompt,
        url
    ):

        print("\n" + "=" * 60)
        print("AI WEB TESTING WORKFLOW")
        print("=" * 60)

        # ==================================================
        # STEP 0
        # EXTRACT TEST CREDENTIALS
        # ==================================================

        credentials = (
            self.extract_credentials(
                user_prompt
            )
        )

        if credentials.get(
            "username"
        ):

            print(
                "\nTest username detected."
            )

            print(
                f"Username: "
                f"{credentials['username']}"
            )

        if credentials.get(
            "password"
        ):

            print(
                "Test password detected."
            )

        # ==================================================
        # STEP 1
        # INSPECT WEBPAGE
        # ==================================================

        print(
            "\n[1] Inspecting webpage..."
        )

        page_data = (
            self.inspector.inspect(
                url
            )
        )

        # ==================================================
        # INSPECTION ERROR
        # ==================================================

        if page_data.get(
            "error"
        ):

            return {
                "status": "FAILED",
                "error": (
                    "Browser inspection failed:\n"
                    + str(
                        page_data.get(
                            "error"
                        )
                    )
                )
            }

        # ==================================================
        # STEP 2
        # STORE PAGE SNAPSHOT
        # ==================================================

        print(
            "\n[2] Storing page snapshot..."
        )

        try:

            snapshot_path = (
                self.page_store.save(
                    page_data
                )
            )

            print(
                "Page snapshot saved:"
            )

            print(
                snapshot_path
            )

        except Exception as e:

            return {
                "status": "FAILED",
                "error": (
                    "Page storage failed:\n"
                    + str(e)
                )
            }

        # ==================================================
        # PAGE INFORMATION
        # ==================================================

        print(
            "\nPage Information:"
        )

        print(
            "-" * 60
        )

        print(
            f"URL   : "
            f"{page_data.get('url')}"
        )

        print(
            f"Title : "
            f"{page_data.get('title')}"
        )

        # ==================================================
        # DISCOVERED ELEMENTS
        # ==================================================

        elements = page_data.get(
            "elements",
            []
        )

        print(
            "\nDiscovered Elements:"
        )

        print(
            "-" * 60
        )

        for index, element in enumerate(
            elements,
            start=1
        ):

            print(
                f"\n{index}. "
                f"{element.get('tag')}"
            )

            print(
                f"   ID            : "
                f"{element.get('id')}"
            )

            print(
                f"   Name          : "
                f"{element.get('name')}"
            )

            print(
                f"   Type          : "
                f"{element.get('type')}"
            )

            print(
                f"   Placeholder   : "
                f"{element.get('placeholder')}"
            )

            print(
                f"   Aria Label    : "
                f"{element.get('aria_label')}"
            )

            print(
                f"   Role          : "
                f"{element.get('role')}"
            )

            print(
                f"   Text          : "
                f"{element.get('text')}"
            )

            print(
                f"   Href          : "
                f"{element.get('href')}"
            )

            print(
                f"   CSS           : "
                f"{element.get('css_selector')}"
            )

            print(
                f"   XPath         : "
                f"{element.get('xpath')}"
            )

            print(
                f"   Playwright    : "
                f"{element.get('playwright_locator')}"
            )

            print(
                f"   Visible       : "
                f"{element.get('visible')}"
            )

            print(
                f"   Enabled       : "
                f"{element.get('enabled')}"
            )

        print(
            f"\nTotal elements discovered: "
            f"{len(elements)}"
        )

        # ==================================================
        # STEP 3
        # LOAD STORED SNAPSHOT
        # ==================================================

        print(
            "\n[3] Loading stored page snapshot..."
        )

        stored_page = (
            self.page_store.load(
                url
            )
        )

        if stored_page is None:

            return {
                "status": "FAILED",
                "error": (
                    "Stored page snapshot "
                    "could not be loaded."
                )
            }

        print(
            "Stored page snapshot loaded."
        )

        # ==================================================
        # STEP 4
        # GENERATE TEST CASES
        # ==================================================

        print(
            "\n[4] Qwen3 generating test cases..."
        )

        try:

            test_cases = (
                self.generator.generate_test_cases(
                    user_prompt=user_prompt,
                    url=url,
                    page_data=stored_page,
                    credentials=credentials
                )
            )

        except Exception as e:

            return {
                "status": "FAILED",
                "error": (
                    "Test case generation failed:\n"
                    + str(e)
                ),
                "url": url,
                "elements": elements,
                "snapshot": snapshot_path
            }

        # ==================================================
        # STEP 5
        # GENERATE PLAYWRIGHT
        # ==================================================

        print(
            "\n[5] Qwen3 generating "
            "Playwright automation..."
        )

        try:

            playwright_code = (
                self.generator.generate_playwright(
                    user_prompt=user_prompt,
                    url=url,
                    page_data=stored_page,
                    test_cases=test_cases,
                    credentials=credentials
                )
            )

        except Exception as e:

            return {
                "status": "FAILED",
                "error": (
                    "Playwright generation failed:\n"
                    + str(e)
                ),
                "url": url,
                "elements": elements,
                "test_cases": test_cases,
                "snapshot": snapshot_path
            }

        # ==================================================
        # STEP 6
        # EXECUTE PLAYWRIGHT
        # ==================================================

        print(
            "\n[6] Executing Playwright automation..."
        )

        execution_result = (
            self.executor.execute(
                playwright_code
            )
        )

        # ==================================================
        # EXECUTION RESULT
        # ==================================================

        if execution_result.get(
            "success"
        ):

            print(
                "\nPlaywright automation PASSED."
            )

        else:

            print(
                "\nPlaywright automation FAILED."
            )

        # ==================================================
        # RETURN RESULT
        # ==================================================

        return {

            "status": execution_result.get(
                "status",
                "FAILED"
            ),

            "url": url,

            "title": (
                stored_page.get(
                    "title"
                )
            ),

            "elements": (
                stored_page.get(
                    "elements",
                    []
                )
            ),

            "test_cases": test_cases,

            "playwright_code": (
                playwright_code
            ),

            "execution": execution_result,

            "snapshot": snapshot_path
        }

    # ======================================================
    # EXTRACT CREDENTIALS
    # ======================================================

    def extract_credentials(
        self,
        user_prompt
    ):

        username = None
        password = None

        # --------------------------------------------------
        # Username patterns
        # --------------------------------------------------

        username_patterns = [

            r'username\s*(?:is|=|:|-)?\s*["\']?([A-Za-z0-9_.@-]+)',
            r'user\s*name\s*(?:is|=|:|-)?\s*["\']?([A-Za-z0-9_.@-]+)',
            r'user\s*(?:is|=|:|-)\s*["\']?([A-Za-z0-9_.@-]+)'
        ]

        for pattern in username_patterns:

            match = re.search(
                pattern,
                user_prompt,
                re.IGNORECASE
            )

            if match:

                username = match.group(
                    1
                ).strip(
                    "\"'"
                )

                break

        # --------------------------------------------------
        # Password patterns
        # --------------------------------------------------

        password_patterns = [

            r'password\s*(?:is|=|:|-)?\s*["\']?([^\s,"\']+)',
            r'pass\s*(?:is|=|:|-)?\s*["\']?([^\s,"\']+)'
        ]

        for pattern in password_patterns:

            match = re.search(
                pattern,
                user_prompt,
                re.IGNORECASE
            )

            if match:

                password = match.group(
                    1
                ).strip(
                    "\"'"
                )

                break

        return {
            "username": username,
            "password": password
        }