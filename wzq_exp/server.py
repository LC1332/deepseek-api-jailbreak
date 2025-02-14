import openai

class Server:
    url = None
    model = None

    def __init__(self, key):
        self.key = key
        self.client = openai.OpenAI(api_key=self.key, base_url=self.url)
        self.content = None

    def send_message(self, msg):
        self.content = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": msg}]
        )

    def get_response(self):
        return self.content

class SiliconFlow(Server):
    model = "deepseek-ai/DeepSeek-V3"
    url = "https://api.siliconflow.cn/v1"
    
    def get_response(self):
        return self.content.choices[0].message.content if self.content else None

class ImyAI(Server):
    model = "deepseek-v3"
    url = "https://api.imyaigc.top"
