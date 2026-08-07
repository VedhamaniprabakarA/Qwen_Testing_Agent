from tools.base_tool import BaseTool


class APITestGenerator(BaseTool):

    def __init__(self, llm):
        self.llm = llm

    def execute(self, requirement):

        prompt = f"""
Generate REST API test cases.

Requirement

{requirement}

Cover

GET

POST

PUT

DELETE

Negative

Boundary

Authorization
"""

        return self.llm.ask(prompt)