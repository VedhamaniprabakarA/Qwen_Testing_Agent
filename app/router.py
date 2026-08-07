from tools.test_case_generator import TestCaseGenerator
from tools.selenium_generator import SeleniumGenerator
from tools.api_test_generator import APITestGenerator
from tools.bug_analyzer import BugAnalyzer


class Router:

    def __init__(self, llm):

        self.tools = {
            "testcase": TestCaseGenerator(llm),
            "selenium": SeleniumGenerator(llm),
            "api": APITestGenerator(llm),
            "bug": BugAnalyzer(llm)
        }

    def route(self, intent, prompt):

        if intent in self.tools:
            return self.tools[intent].execute(prompt)

        return None