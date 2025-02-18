from openai import OpenAI
from dotenv import load_dotenv
import os

def question2response(user_input):
    deepseek_api_key = os.getenv("SILICONFLOW_API_KEY")
    client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")  # 创建客户端实例

    response = client.chat.completions.create(  # 发送请求
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": user_input}
        ],
        stream=False,
        response_format={
            'type': 'json_object'
        }
    )

    return response.choices[0].message.content  # 返回AI的回答内容

if __name__ == "__main__":
    # 加载环境变量
    load_dotenv()
    
    # 测试问题
    test_question = "请用JSON格式回答：你最喜欢的三种水果是什么？"
    
    try:
        # 调用函数并获取响应
        response = question2response(test_question)
        print("AI的回答：")
        print(response)
        
    except Exception as e:
        print(f"发生错误：{str(e)}")
