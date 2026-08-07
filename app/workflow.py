from tools.test_case_generator import TestCaseGenerator
from tools.selenium_generator import SeleniumGenerator
from tools.api_test_generator import APITestGenerator
from tools.bug_analyzer import BugAnalyzer


class Workflow:

    def __init__(self, llm):

        self.testcase_generator = TestCaseGenerator(llm)
        self.selenium_generator = SeleniumGenerator(llm)
        self.api_generator = APITestGenerator(llm)
        self.bug_analyzer = BugAnalyzer(llm)

    def run(self, url, prompt):

        result = {
            "url": url,
            "prompt": prompt
        }

        # Step 1
        testcase = self.testcase_generator.execute(
            f"""
Website:
{url}

Requirement:
{prompt}
"""
        )

        result["test_cases"] = testcase

        # Step 2
        selenium = self.selenium_generator.execute(
            f"""
Website:
{url}

Test Cases:
{testcase}
"""
        )

        result["selenium_code"] = selenium

        # Future Steps
        # result["website_analysis"] = ...
        # result["playwright_code"] = ...
        # result["execution"] = ...
        # result["report"] = ...

        return result