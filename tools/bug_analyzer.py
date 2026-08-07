from tools.base_tool import BaseTool


class BugAnalyzer(BaseTool):

    def __init__(self, llm):
        self.llm = llm

    def execute(self, stacktrace):

        prompt = f"""
Analyze this exception.

Explain

Root Cause

Likely Reason

Possible Fix

Code Improvement

Stacktrace

{stacktrace}
"""

        return self.llm.ask(prompt)