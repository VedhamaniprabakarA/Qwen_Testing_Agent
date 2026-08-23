from tools.browser_inspector import BrowserInspector
from tools.web_test_generator import WebTestGenerator
from tools.playwright_validator import PlaywrightValidator
from tools.page_store import PageStore


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
        # PLAYWRIGHT VALIDATOR
        # ==================================================

        self.validator = PlaywrightValidator()

        # ==================================================
        # PAGE STORAGE
        # ==================================================

        self.page_store = PageStore()

    # ======================================================
    # MAIN WORKFLOW
    # ======================================================

    def execute(self, url):

        print("\n" + "=" * 60)
        print("AI WEB TESTING WORKFLOW")
        print("=" * 60)

        # ==================================================
        # STEP 1 - INSPECT WEBSITE
        # ==================================================

        print("\n[1] Inspecting webpage...")

        page_data = self.inspector.inspect(
            url
        )

        # ==================================================
        # CHECK INSPECTION ERROR
        # ==================================================

        if page_data.get("error"):

            return {
                "status": "FAILED",
                "error": (
                    "Browser inspection failed:\n"
                    + str(
                        page_data.get("error")
                    )
                )
            }

        # ==================================================
        # STEP 2 - STORE PAGE SNAPSHOT
        # ==================================================

        print(
            "\n[2] Storing inspected "
            "page specification..."
        )

        try:

            snapshot_path = (
                self.page_store.save(
                    page_data
                )
            )

            print(
                f"Page snapshot saved:"
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
        # PRINT PAGE INFORMATION
        # ==================================================

        print("\nPage Information:")
        print("-" * 60)

        print(
            f"URL   : "
            f"{page_data.get('url')}"
        )

        print(
            f"Title : "
            f"{page_data.get('title')}"
        )

        # ==================================================
        # GET ELEMENTS
        # ==================================================

        elements = page_data.get(
            "elements",
            []
        )

        # ==================================================
        # PRINT DISCOVERED ELEMENTS
        # ==================================================

        print("\nDiscovered Elements:")
        print("-" * 60)

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
        # STEP 3 - LOAD STORED PAGE
        # ==================================================

        print(
            "\n[3] Loading stored "
            "page specification..."
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
                    "Stored page specification "
                    "could not be loaded."
                )
            }

        print(
            "Stored page loaded successfully."
        )

        # ==================================================
        # STEP 4 - GENERATE TEST CASES
        # ==================================================

        print(
            "\n[4] Qwen3 generating "
            "test cases..."
        )

        try:

            test_cases = (
                self.generator.generate_test_cases(
                    url,
                    stored_page
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
        # STEP 5 - GENERATE PLAYWRIGHT
        # ==================================================

        print(
            "\n[5] Qwen3 generating "
            "Playwright automation..."
        )

        try:

            playwright_code = (
                self.generator.generate_playwright(
                    url,
                    stored_page,
                    test_cases
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
        # STEP 6 - VALIDATE AGAINST STORED PAGE
        # ==================================================

        print(
            "\n[6] Validating generated "
            "Playwright code..."
        )

        validation = (
            self.validator.validate(
                playwright_code,
                url,
                stored_page
            )
        )

        # ==================================================
        # VALIDATION RESULT
        # ==================================================

        if validation.get("valid"):

            print(
                "\nValidation PASSED."
            )

        else:

            print(
                "\nValidation FAILED."
            )

            print(
                "\nValidation Errors:"
            )

            for error in validation.get(
                "errors",
                []
            ):

                print(
                    f" - {error}"
                )

            # ==================================================
            # STEP 7 - ASK QWEN TO CORRECT
            # ==================================================

            print(
                "\n[7] Asking Qwen3 to "
                "correct the script..."
            )

            correction_prompt = (
                self.build_correction_prompt(
                    url,
                    stored_page,
                    validation,
                    playwright_code
                )
            )

            try:

                corrected_code = (
                    self.generator.model.ask(
                        correction_prompt
                    )
                )

                # ------------------------------------------
                # Clean code
                # ------------------------------------------

                corrected_code = (
                    self.clean_code(
                        corrected_code
                    )
                )

                # ------------------------------------------
                # Validate corrected code
                # ------------------------------------------

                print(
                    "\n[8] Re-validating "
                    "corrected script..."
                )

                second_validation = (
                    self.validator.validate(
                        corrected_code,
                        url,
                        stored_page
                    )
                )

                if second_validation.get(
                    "valid"
                ):

                    print(
                        "\nCorrected script "
                        "PASSED validation."
                    )

                    playwright_code = (
                        corrected_code
                    )

                    validation = (
                        second_validation
                    )

                else:

                    print(
                        "\nCorrected script "
                        "still FAILED validation."
                    )

                    for error in (
                        second_validation.get(
                            "errors",
                            []
                        )
                    ):

                        print(
                            f" - {error}"
                        )

                    playwright_code = (
                        corrected_code
                    )

                    validation = (
                        second_validation
                    )

            except Exception as e:

                print(
                    "\nCode correction failed:"
                )

                print(
                    str(e)
                )

        # ==================================================
        # FINAL STATUS
        # ==================================================

        final_status = (
            "PASSED"
            if validation.get("valid")
            else "VALIDATION_FAILED"
        )

        # ==================================================
        # RETURN RESULT
        # ==================================================

        return {

            "status": final_status,

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

            "validation": validation,

            "snapshot": snapshot_path
        }

    # ======================================================
    # BUILD CORRECTION PROMPT
    # ======================================================

    def build_correction_prompt(
        self,
        url,
        stored_page,
        validation,
        playwright_code
    ):

        elements = stored_page.get(
            "elements",
            []
        )

        return f"""
You are a senior Python Playwright automation engineer.

The generated Playwright script failed validation.

==================================================
REAL TARGET URL
==================================================

{url}

==================================================
STORED PAGE SPECIFICATION
==================================================

{elements}

==================================================
VALIDATION ERRORS
==================================================

{validation.get("errors", [])}

==================================================
GENERATED SCRIPT
==================================================

{playwright_code}

==================================================
STRICT RULES
==================================================

1. The target URL MUST remain exactly:

{url}

2. Never use example.com.

3. Never use another website.

4. Never invent elements.

5. Never invent IDs.

6. Never invent names.

7. Never invent CSS selectors.

8. Never invent XPath.

9. Never invent URLs.

10. Never invent pages.

11. Never invent dashboard/profile/settings
    elements unless they exist in the stored
    page specification.

12. Use only elements from the stored page
    specification.

13. Prefer the exact Playwright locator
    provided by the stored element.

14. Prefer:

    page.get_by_role()

15. Prefer:

    page.get_by_label()

16. Prefer:

    page.get_by_placeholder()

17. Use CSS only when necessary.

18. Use XPath only as a last resort.

19. Use Python Playwright.

20. Use sync_playwright.

21. Launch Chromium with:

    headless=False

22. Do not use Selenium.

23. Do not use requests.

24. Return ONLY executable Python code.

==================================================
TASK
==================================================

Correct the generated script based ONLY on
the stored page specification and validation
errors.

Return ONLY Python code.
"""

    # ======================================================
    # CLEAN QWEN CODE
    # ======================================================

    def clean_code(
        self,
        code
    ):

        if not code:

            return ""

        code = code.strip()

        # --------------------------------------------------
        # Remove ```python
        # --------------------------------------------------

        if code.startswith(
            "```python"
        ):

            code = code[
                len("```python"):
            ]

        # --------------------------------------------------
        # Remove ```
        # --------------------------------------------------

        if code.startswith(
            "```"
        ):

            code = code[
                len("```"):
            ]

        if code.endswith(
            "```"
        ):

            code = code[
                :-len("```")
            ]

        return code.strip()