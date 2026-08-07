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