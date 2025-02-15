import openai

class Server:
    def __init__(self, key, model, url):
        self.key = key
        self.model = model  # Ensure model is set
        self.url = url
        self.client = openai.OpenAI(api_key=self.key, base_url=self.url)
        self.content = None

    def send_message(self, msg):
        if not self.model:
            raise ValueError("Model is not set. Please specify a valid model.")
        
        self.content = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": msg}]
        )

    def send_conversation(self, conv):
        if not self.model:
            raise ValueError("Model is not set. Please specify a valid model.")
        
        self.content = self.client.chat.completions.create(
            model=self.model,
            messages=conv  # Pass the conversation messages list
        )


    def get_response(self):
        return self.content.choices[0].message.content if self.content else None

# Subclasses inherit from Server
class SiliconFlow(Server):
    def __init__(self, key):
        super().__init__(key, "deepseek-ai/DeepSeek-V3", "https://api.siliconflow.cn/v1")

class ImyAI(Server):
    def __init__(self, key):
        super().__init__(key, "deepseek-v3", "https://api.imyaigc.top")

class VolcanoAI(Server):
    def __init__(self, key):
        super().__init__(key, "ep-20250215104522-c2wll", "https://ark.cn-beijing.volces.com/api/v3")
