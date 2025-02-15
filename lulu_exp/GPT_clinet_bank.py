class GPTClientBase:
    def __init__(self):
        pass

    def message2response( self, messages: list , max_output_tokens: int = -1 ) -> str:
        # for idel output simply return the last message's content
        if len(messages) > 0 and messages[-1]["role"] == "user":
            return messages[-1]["content"]
        else:
            return "hello, now runing GPT client base class"

def get_gpt_clients() -> list:
    return [
        ("DeepSeek-V3", GPTClientBase()),
        ("DeepSeek-R1", GPTClientBase()),
        ("GLM-4-Air", GPTClientBase()),
    ]

def get_gpt_client_dict() -> dict:
    clients = get_gpt_clients()
    return {client[0]: client[1] for client in clients}


if __name__ == "__main__":
    print(get_gpt_clients())
