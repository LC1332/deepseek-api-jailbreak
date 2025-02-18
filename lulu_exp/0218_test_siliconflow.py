from GPT_clinet_bank import *

SiliconFlow=GPTClientBase(key=os.getenv("SILICONFLOW_API_KEY"), model="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B", url="https://api.siliconflow.cn/v1")

query = "爸爸的爸爸叫什么"

response = SiliconFlow.send_message(query)

print(response)