from tools.base_tool import BaseTool


class TestCaseGenerator(BaseTool):

    def __init__(self, llm):
        self.llm = llm

    def execute(self, requirement):

        prompt = f"""
You are a Senior QA Engineer.

Generate professional manual test cases.

Requirement:

{requirement}

Return the output in markdown table.

Columns:

Test Case ID
Title
Precondition
Steps
Expected Result
Priority
"""

        return self.llm.ask(prompt)

    def generate_test_cases(
        self,
        url,
        page_data
    ):

        elements = self.format_elements(
            page_data
        )

        prompt = f"""
    You are a strict software testing engineer.

    TARGET WEBSITE:
    {url}

    PAGE TITLE:
    {page_data.get("title")}

    ACTUAL DISCOVERED ELEMENTS:
    {elements}

    IMPORTANT RULES:

    1. The TARGET WEBSITE URL must NEVER be changed.

    2. You may ONLY reference elements explicitly
    present in ACTUAL DISCOVERED ELEMENTS.

    3. NEVER invent:
    - IDs
    - names
    - classes
    - buttons
    - links
    - URLs
    - fields
    - selectors
    - pages
    - error messages

    4. If an element does not exist in the discovered
    elements, DO NOT create a test case for it.

    5. Do not assume an element exists because it is
    common on login pages.

    6. For the Login button, use its actual discovered
    properties.

    7. For username, use the actual discovered
    username element.

    8. For password, use the actual discovered
    password element.

    Generate functional test cases.

    Focus on:
    - Valid login
    - Invalid login
    - Empty username
    - Empty password
    - Empty credentials
    - Login button behavior
    - Existing links
    - Existing navigation

    For each test case provide:

    TEST CASE ID
    TEST CASE NAME
    PRECONDITION
    STEPS
    TEST DATA
    EXPECTED RESULT

    Do not invent UI elements.

    If an expected result cannot be verified from the
    discovered DOM, describe it as a URL/page-state
    assertion rather than inventing an error element.
    """

        return self.model.ask(prompt)