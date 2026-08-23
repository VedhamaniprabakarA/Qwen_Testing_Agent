import re

from models.llama_model import LlamaModel
from app.intent_classifier import IntentClassifier
from app.router import Router
from app.browser_workflow import BrowserWorkflow


class TestingAgent:

    def __init__(self):

        self.model = LlamaModel()

        self.intent = IntentClassifier()

        self.router = Router(
            self.model
        )

        self.browser_workflow = (
            BrowserWorkflow()
        )

    def chat(self, user_input):

        # ==========================================
        # CHECK FOR URL
        # ==========================================

        url_match = re.search(
            r'https?://[^\s]+',
            user_input
        )

        browser_keywords = [
            "test this page",
            "test this website",
            "test this login",
            "automate this page",
            "automate this website",
            "playwright",
            "web testing",
            "test the webpage",
            "test webpage",
            "login page"
        ]

        is_browser_test = (
            url_match is not None
            and any(
                keyword in user_input.lower()
                for keyword in browser_keywords
            )
        )

        # ==========================================
        # BROWSER TESTING
        # ==========================================

        if is_browser_test:

            url = url_match.group(0)

            return self.browser_workflow.execute(
                url
            )

        # ==========================================
        # EXISTING AGENT
        # ==========================================

        intent = self.intent.classify(
            user_input
        )

        result = self.router.route(
            intent,
            user_input
        )

        if result:
            return result

        return self.model.ask(
            user_input
        )