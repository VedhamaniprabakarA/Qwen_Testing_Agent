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

    # ======================================================
    # CHAT
    # ======================================================

    def chat(
        self,
        user_input
    ):

        # ==================================================
        # CHECK FOR URL
        # ==================================================

        url_match = re.search(
            r'https?://[^\s]+',
            user_input
        )

        # ==================================================
        # BROWSER TESTING KEYWORDS
        # ==================================================

        browser_keywords = [

            "test this page",
            "test this website",
            "test this login",
            "test login",
            "automate this page",
            "automate this website",
            "automate the page",
            "playwright",
            "web testing",
            "test the webpage",
            "test webpage",
            "login page",
            "test the login"
        ]

        is_browser_test = (
            url_match is not None
            and any(
                keyword in user_input.lower()
                for keyword in browser_keywords
            )
        )

        # ==================================================
        # BROWSER TESTING
        # ==================================================

        if is_browser_test:

            url = url_match.group(0)

            # Remove trailing punctuation
            url = url.rstrip(
                ".,;:)"
            )

            print(
                "\nBrowser testing request detected."
            )

            print(
                f"Target URL: {url}"
            )

            # IMPORTANT:
            # Pass the COMPLETE user request.
            #
            # This allows the workflow/generator
            # to receive:
            #
            # URL
            # Username
            # Password
            # Test requirements
            #
            return self.browser_workflow.execute(
                user_prompt=user_input,
                url=url
            )

        # ==================================================
        # EXISTING AGENT
        # ==================================================

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