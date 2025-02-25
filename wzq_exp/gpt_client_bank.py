import openai
import os
import httpx

no_proxy_client = httpx.Client(transport=httpx.HTTPTransport(proxy=None))

class GPTClientBase:
    def __init__(self, *args):
        self.key, self.model, self.url, self.provider = args[0], args[1], args[2], args[3] if len(args) > 3 else None
        self.client = openai.OpenAI(api_key=self.key, base_url=self.url, http_client=no_proxy_client)
        self.content = None

    def send_text(self, msg):
        attempts = 0
        while attempts < 5:
            try:
                self.content = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": msg}]
                )
                return self.get_response()
            except Exception as e:
                attempts += 1
                if attempts >= 5:
                    raise e

    def send_messages(self, conv):
        attempts = 0
        while attempts < 5:
            try:
                self.content = self.client.chat.completions.create(
                    model=self.model,
                    messages=conv  # Pass the conversation messages list
                )
                return self.get_response()
            except Exception as e:
                attempts += 1
                if attempts >= 5:
                    raise e

    def get_response(self):
        return self.content.choices[0].message.content if self.content else None

from dotenv import load_dotenv
load_dotenv()

SiliconFlow1 = GPTClientBase(os.getenv("SILICONFLOW_API_KEY"), "deepseek-ai/DeepSeek-R1", "https://api.siliconflow.cn/v1", "硅基流动")
SiliconFlow2 = GPTClientBase(os.getenv("SILICONFLOW_API_KEY"), "deepseek-ai/DeepSeek-V3", "https://api.siliconflow.cn/v1", "硅基流动")
VolcanoAI1 = GPTClientBase(os.getenv("VOLCANO_API_KEY"), "ep-20250215104522-c2wll", "https://ark.cn-beijing.volces.com/api/v3", "火山方舟")
VolcanoAI2 = GPTClientBase(os.getenv("VOLCANO_API_KEY"), "ep-20250215164946-8wkww", "https://ark.cn-beijing.volces.com/api/v3", "火山方舟")
GLM = GPTClientBase(os.getenv("GLM_API_KEY"), "glm-4-air", "https://open.bigmodel.cn/api/paas/v4/", "智谱")
ALI1 = GPTClientBase(os.getenv("ALI_API_KEY"), "deepseek-r1", "https://dashscope.aliyuncs.com/compatible-mode/v1", "阿里云")
ALI2 = GPTClientBase(os.getenv("ALI_API_KEY"), "deepseek-v3", "https://dashscope.aliyuncs.com/compatible-mode/v1", "阿里云")
TEN1 = GPTClientBase(os.getenv("TEN_API_KEY"), "deepseek-r1", "https://api.lkeap.cloud.tencent.com/v1", "腾讯云")
TEN2 = GPTClientBase(os.getenv("TEN_API_KEY"), "deepseek-v3", "https://api.lkeap.cloud.tencent.com/v1", "腾讯云")

def get_gpt_clients() -> list:
    return [
        #("GLM-4-Air", GLM),
        #("火山方舟DeepSeek-R1", VolcanoAI1),
        #("火山方舟DeepSeek-V3", VolcanoAI2),
        ("阿里云DeepSeek-R1", ALI1),
        ("阿里云DeepSeek-V3", ALI2),
        #("腾讯云DeepSeek-R1",TEN1),
        #("腾讯云DeepSeek-V3",TEN2),
        #("硅基流动DeepSeek-R1", SiliconFlow1),
        #("硅基流动DeepSeek-V3", SiliconFlow2),
    ]

def get_gpt_client_dict() -> dict:
    clients = get_gpt_clients()
    return {client[0]: client[1] for client in clients}

if __name__ == "__main__":
    client_dict = get_gpt_client_dict()
    model = "腾讯云DeepSeek-V3"
    client = client_dict[model]
    response = client.send_text("hello")
    print(response)
