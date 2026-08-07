from langchain_ollama import ChatOllama

class LlamaModel:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen3:4b",
            temperature=0
        )

    def ask(self, prompt):
        response = self.llm.invoke(prompt)
        return response.content