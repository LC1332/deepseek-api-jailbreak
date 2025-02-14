import requests
class Server:
    url=None
    model=None
    def __init__(self,key):
        self.key=key
    def send_message(self,msg):
        payload = {
            "model": self.model,
            "messages": [
                {
                    "content": msg,
                    "role": "user"
                }
            ]
        }
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
        response = requests.request("POST", self.url, json=payload, headers=headers)
        self.content=response
        
    def get_response(self):
        return self.content

class siliconflow(Server):
    model="deepseek-ai/DeepSeek-V3"
    url="https://api.siliconflow.cn/v1/chat/completions"
    def get_response(self):
        response_json=self.content.json()
        return response_json["choices"][0]["message"]["content"]

class imyai(Server):
    model="deepseek-v3"
    url="https://api.imyaigc.top"