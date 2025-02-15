from GPT_clinet_bank import get_gpt_client_dict
from meta_prompt_bank import get_transfer_funcs


def message2text( messages: list ) -> str:
    if len(messages) == 1:
        return messages[0]["content"]
    else:
        ans = ""
        for message in messages:
            ans += f"{message['role']}: {message['content']}\n"
        return ans


def text2translate_message( text: str ) -> list:
    return [
        {"role": "user", "content": f"将反引号中的内容翻译成中文: ```{text}```"}
    ]

if __name__ == "__main__":
    client_dict = get_gpt_client_dict()
    model_names = list(client_dict.keys())

    meta_prompt_bank = get_transfer_funcs( output_format = "message" )

    transfer_meta_names = [x[0] for x in meta_prompt_bank]
    transfer_meta_prompts = [x[1] for x in meta_prompt_bank]

    query = "I want to buy a car"

    selected_transfer_meta_name = "method_k3"

    selected_meta_prompt = transfer_meta_prompts[transfer_meta_names.index(selected_transfer_meta_name)]

    transfer_message = selected_meta_prompt(query)

    # display_message = message2text(transfer_message)
    # print("转化用的prompt",display_message)

    transfer_model = "DeepSeek-V3" if "DeepSeek" in model_names else model_names[0]
    translate_model = "GLM-4-Air" if "GLM-4-Air" in model_names else model_names[0]
    jailbreak_model = "DeepSeek-R1" if "DeepSeek-R1" in model_names else model_names[0]

    transfer_client = client_dict[transfer_model]

    transferred_prompt = transfer_client.message2response(transfer_message)

    transferred_message = [{"role": "user", "content": transferred_prompt}]

    print("转化后的prompt:")

    print(transferred_prompt)

    print("转化后的prompt翻译成中文:")

    translate_client = client_dict[translate_model]

    translated_prompt = translate_client.message2response(text2translate_message(transferred_prompt))

    print(translated_prompt)

    print("用转化后的prompt进行query")

    jailbreak_client = client_dict[jailbreak_model]

    jailbreak_response = jailbreak_client.message2response(transferred_message)

    print("jailbreak response:")

    print(jailbreak_response)

    print("翻译成中文的jailbreak response")

    translated_jailbreak_response = translate_client.message2response(text2translate_message(jailbreak_response))

    print(translated_jailbreak_response)
