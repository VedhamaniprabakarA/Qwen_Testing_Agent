from app.agent import TestingAgent

def main():

    agent = TestingAgent()

    print("=" * 60)
    print("AI Software Testing Agent")
    print("=" * 60)

    while True:

        prompt = input("\nYou: ")

        if prompt.lower() == "exit":
            break

        response = agent.chat(prompt)

        print("\nAgent:")
        print(response)


if __name__ == "__main__":
    main()