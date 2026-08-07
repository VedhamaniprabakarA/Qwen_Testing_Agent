from models.llama_model import LlamaModel
from app.intent_classifier import IntentClassifier
from app.router import Router
'''class TestingAgent:

    def __init__(self):
        self.model = LlamaModel()

    def chat(self, prompt):
        return self.model.ask(prompt) 
    
    from models.llama_model import LlamaModel
from app.intent_classifier import IntentClassifier
from app.router import Router
'''

class TestingAgent:

    def __init__(self):
        self.model = LlamaModel()
        self.intent = IntentClassifier()
        self.router = Router(self.model)

    def chat(self, user_input):

        intent = self.intent.classify(user_input)

        result = self.router.route(intent, user_input)

        if result:
            return result

        return self.model.ask(user_input)