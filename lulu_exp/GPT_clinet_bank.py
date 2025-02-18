from dotenv import load_dotenv
import os

# set proxy port to 8234
os.environ["http_proxy"] = "http://127.0.0.1:8234"
os.environ["https_proxy"] = "http://127.0.0.1:8234"

import openai


class GPTClientBase:
    def __init__(self, key, model, url):
        self.key = key
        self.model = model  # Ensure model is set
        self.url = url
        self.client = openai.OpenAI(api_key=self.key, base_url=self.url)
        self.content = None

    def send_message(self, msg):
        self.content = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": msg}]
        )
        return self.get_response()

    def send_conversation(self, conv):
        self.content = self.client.chat.completions.create(
            model=self.model,
            messages=conv  # Pass the conversation messages list
        )
        return self.get_response()


    def generate(self,conv,max_retries=5):
        attempts = 0

        while attempts < max_retries:
            try:
                self.send_conversation(conv)
                
                response = self.get_response()

                # if success, break out of the loop
                break
            except Exception as e:
                attempts += 1
                if attempts >= max_retries:
                    raise e  # if max_retries reached, raise the exception
        return response
    
    def get_response(self):
        return self.content.choices[0].message.content if self.content else None

load_dotenv()

SiliconFlow=GPTClientBase(key=os.getenv("SILICONFLOW_API_KEY"), model="deepseek-ai/DeepSeek-V3", url="https://api.siliconflow.cn/v1")

VolcanoAI=GPTClientBase(key=os.getenv("VOLCANO_API_KEY"),model="ep-20250215104522-c2wll", url="https://ark.cn-beijing.volces.com/api/v3")

JudgeAI=GPTClientBase(key=os.getenv("ARK_API_KEY"), model="ep-20250215164946-8wkww", url="https://ark.cn-beijing.volces.com/api/v3")

GLM=GPTClientBase(key=os.getenv("GLM_API_KEY"),model="glm-4-air",url="https://open.bigmodel.cn/api/paas/v4/chat/completions")

def get_gpt_clients() -> list:
    return [
        ("DeepSeek-V3", SiliconFlow),
        ("DeepSeek-R1", VolcanoAI),
        ("Judge", JudgeAI),
        ("GLM-4-Air", GLM),
    ]

def get_gpt_client_dict() -> dict:
    clients = get_gpt_clients()
    return {client[0]: client[1] for client in clients}


if __name__ == "__main__":
    print(get_gpt_clients())
