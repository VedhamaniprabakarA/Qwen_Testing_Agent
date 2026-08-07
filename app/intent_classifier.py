class IntentClassifier:

    def classify(self, text):

        text = text.lower()

        if "selenium" in text:
            return "selenium"

        if "playwright" in text:
            return "playwright"

        if "api" in text:
            return "api"

        if "sql" in text:
            return "sql"

        if "bug" in text or "exception" in text:
            return "bug"

        if "test case" in text:
            return "testcase"

        return "chat"