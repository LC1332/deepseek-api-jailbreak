'''
0215_simple_pipeline.py中的代码可以顺利运行

我需要将这个代码转化为一个简易的gradio的界面

gradio的界面分类两列

# 界面

## 左侧

- query的输入 input

- 转换按钮，按下后将 input 转化为 transferred_message

- text area 显示 transferred_message 

- query 按钮和翻译按钮
    - query 按下后用transferred_message进行query，同时transferred_message和query都会显示在右侧的chatbot中
    - 翻译按下，如果chatbot是空的，则翻译transferred_message， 如果chatbot不是空的，则翻译最后一条信息

- text area 显示翻译的message

- 下面是三组radios，分别是transfer方法选择， transfer模型选择和翻译模型选择

## 右侧

- 高度为800的chatbot，

- 文本输入框和输入按钮，可以根据history进一步对chatbot中的内容进行追问

- 下面一组radio，是chat模型（代码中为jailbreak模型）选择
'''

import gradio as gr
from GPT_clinet_bank import get_gpt_client_dict
from meta_prompt_bank import get_transfer_funcs

# 添加全局变量
client_dict = None
def init_client_dict():
    global client_dict
    if client_dict is None:
        client_dict = get_gpt_client_dict()
    return client_dict

def message2text(messages: list) -> str:
    if len(messages) == 1:
        return messages[0]["content"]
    else:
        ans = ""
        for message in messages:
            ans += f"{message['role']}: {message['content']}\n"
        return ans

def text2translate_message(text: str) -> list:
    return [
        {"role": "user", "content": f"将反引号中的内容翻译成中文: ```{text}```"}
    ]


def transfer_message(query, transfer_method, transfer_model_name):
    global client_dict
    meta_prompt_bank = get_transfer_funcs(output_format="message")
    
    transfer_meta_names = [x[0] for x in meta_prompt_bank]
    transfer_meta_prompts = [x[1] for x in meta_prompt_bank]

    selected_meta_prompt = transfer_meta_prompts[transfer_meta_names.index(transfer_method)]
    transfer_message = selected_meta_prompt(query)

    transfer_client = client_dict[transfer_model_name]
    transferred_prompt = transfer_client.message2response(transfer_message)

    return transferred_prompt
    

def process_query(transferred_text, jailbreak_model, chatbot):
    global client_dict
    transferred_message = [{"role": "user", "content": transferred_text}]
    
    jailbreak_client = client_dict[jailbreak_model]
    jailbreak_response = jailbreak_client.message2response(transferred_message)
    
    chatbot.append((transferred_text, jailbreak_response))
    
    return chatbot

def translate_text(text, translate_model_name, chatbot):
    global client_dict
    translate_client = client_dict[translate_model_name]

    to_translate_text = text
    if len(chatbot) > 0:
        to_translate_text = chatbot[-1][1]

    translated_text = translate_client.message2response(text2translate_message(to_translate_text))
    return translated_text

def chat_follow_up(message, jailbreak_model_name, chatbot):
    global client_dict
    jailbreak_client = client_dict[jailbreak_model_name]
    
    messages = [{"role": "user" if i%2==0 else "assistant", "content": m[1]} for i,m in enumerate(chatbot)]
    messages.append({"role": "user", "content": message})
    
    response = jailbreak_client.message2response(messages)
    chatbot.append((message, response))
    
    return "", chatbot

def create_interface():
    global client_dict
    init_client_dict()  # 初始化client_dict
    
    model_names = list(client_dict.keys())
    meta_prompt_bank = get_transfer_funcs(output_format="message")
    transfer_meta_names = [x[0] for x in meta_prompt_bank]
    
    default_transfer_model = "DeepSeek-V3" if "DeepSeek" in model_names else model_names[0]
    default_translate_model = "GLM-4-Air" if "GLM-4-Air" in model_names else model_names[0]
    default_jailbreak_model = "DeepSeek-R1" if "DeepSeek-R1" in model_names else model_names[0]

    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(label="输入查询")
                transfer_btn = gr.Button("转换")
                transferred_text = gr.TextArea(label="转换后的消息")
                
                with gr.Row():
                    query_btn = gr.Button("开始越狱!")
                    translate_btn = gr.Button("翻译")
                
                translated_text = gr.TextArea(label="翻译后的消息")
                
                transfer_method = gr.Radio(choices=transfer_meta_names, value=transfer_meta_names[0], label="转换方法")
                transfer_model = gr.Radio(choices=model_names, value=default_transfer_model, label="转换模型")
                translate_model = gr.Radio(choices=model_names, value=default_translate_model, label="翻译模型")
            
            with gr.Column():
                chatbot = gr.Chatbot(height=800)
                with gr.Row():
                    chat_input = gr.Textbox(show_label=False)
                    chat_submit = gr.Button("发送")
                
                jailbreak_model = gr.Radio(choices=model_names, value=default_jailbreak_model, label="对话模型")
        
        # 事件处理
        transfer_btn.click(
            transfer_message,
            inputs=[input_text, transfer_method, transfer_model],
            outputs=[transferred_text]
        )
        
        query_btn.click(
            process_query,
            inputs=[transferred_text, jailbreak_model, chatbot],
            outputs=[chatbot]
        )
        
        translate_btn.click(
            translate_text,
            inputs=[transferred_text,  translate_model, chatbot],
            outputs=[translated_text]
        )
        
        chat_input.submit(
            chat_follow_up,
            inputs=[chat_input, jailbreak_model, chatbot],
            outputs=[chat_input, chatbot]
        )
        
        chat_submit.click(
            chat_follow_up,
            inputs=[chat_input, jailbreak_model, chatbot],
            outputs=[chat_input, chatbot]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch()

