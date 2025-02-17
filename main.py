import json
from judges import *
from gpt_client_bank import *
from meta_prompt_bank import *
from prompt_selector import *

client_dict = get_gpt_client_dict()
model_names = list(client_dict.keys())

meta_prompt_bank = get_transfer_funcs(output_format="message")

transfer_meta_names = [x[0] for x in meta_prompt_bank]
transfer_meta_prompts = [x[1] for x in meta_prompt_bank]

selected_transfer_meta_name = "method_k3"
selected_meta_prompt = transfer_meta_prompts[transfer_meta_names.index(selected_transfer_meta_name)]

jailbreak_model = "DeepSeek-R1" if "DeepSeek-R1" in model_names else model_names[0]
jailbreak_client = client_dict[jailbreak_model]

csv_filename = "harmful_behaviors_jailbreakbench.csv"
column_name = "Goal"
selector = PromptSelector(csv_filename, column_name)

output_json = "火山benchmark.json"
results = []

for _ in range(10):
    prompt = selector.get_next_prompt()
    reformulated = selected_meta_prompt(prompt)
    response = jailbreak_client.send_conversation(reformulated)
    judgment = judge_ai(VolcanoAI, prompt, response)
    
    results.append({
        "Prompt": prompt,
        "API provider":jailbreak_client.provider,
        "Model": jailbreak_model,
        "Jailbroken": judgment,
        "Reformulated Prompt": reformulated,
        "Response": response
    })

# Write results to a JSON file
with open(output_json, mode="w", encoding="utf-8") as file:
    json.dump(results, file, ensure_ascii=False, indent=4)

print(f"Results stored in {output_json}")
