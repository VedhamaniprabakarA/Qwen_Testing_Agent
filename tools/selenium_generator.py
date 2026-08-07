from tools.base_tool import BaseTool


class SeleniumGenerator(BaseTool):

    def __init__(self, llm):
        self.llm = llm

    def execute(self, requirement):

        prompt = f"""
Generate Selenium Python code using Page Object Model.

Requirement:

{requirement}

Use

Python

Pytest

Selenium

Explicit Wait

Reusable methods
"""

        return self.llm.ask(prompt)