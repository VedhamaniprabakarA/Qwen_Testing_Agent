from langchain_ollama import ChatOllama


class LlamaModel:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen3:4b",
            base_url="http://127.0.0.1:11434",
            #model="qwen2.5-coder:7b",
            #base_url="http://192.168.1.13:11434",
            temperature=0.2
        )

    def ask(self, prompt):
        response = self.llm.invoke(prompt)
        return response.content