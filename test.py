import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key
api_key = os.getenv("DEEPSEEK_API_KEY")

url = "https://api.siliconflow.cn/v1/chat/completions"

payload = {
    "model": "deepseek-ai/DeepSeek-R1",
    "messages": [
        {
            "content": "hi",
            "role": "user"
        }
    ]
}
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

response_json=response.json()

content = response_json["choices"][0]["message"]["content"]
print(content)

print(response_json["id"])