import json
import csv
import matplotlib.pyplot as plt
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

csv_filename = "./input/10prompts.csv"
column_name = "Goal"

output_json = "jailbroken_results.json"
output_md = "jailbroken_results.md"
results = []

# Clear the content of the JSON file before starting
with open(output_json, mode="w", encoding="utf-8") as file:
    json.dump([], file)

# Write the header to the Markdown file
with open(output_md, mode="w", encoding="utf-8") as file:
    file.write("# Jailbroken Results\n\n")
    file.write("| Model | Prompt | Judgment |\n")
    file.write("|-------|--------|----------|\n")

# Iterate over each model in the client dict
for jailbreak_model in model_names:
    jailbreak_client = client_dict[jailbreak_model]
    print(f"Testing model: {jailbreak_model}")
    judge_client = GLM
    model_results = []
    jailbroken_count = 0
    total_count = 0

    # Read each prompt from the CSV file
    with open(csv_filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            prompt = row[column_name]
            reformulated = selected_meta_prompt(prompt, jailbreak_client)
            
            response = jailbreak_client.send_messages(reformulated)
            judgment = judge_ai(judge_client, prompt, response)
            
            model_results.append({
                "Prompt": prompt,
                "API provider": jailbreak_client.provider,
                "Model": jailbreak_model,
                "Jailbroken": judgment,
                "Reformulated Prompt": reformulated,
                "Response": response
            })

            if judgment:
                jailbroken_count += 1
            total_count += 1

    jailbroken_rate = jailbroken_count / total_count if total_count > 0 else 0
    print(f"Model: {jailbreak_model}, Jailbroken Rate: {jailbroken_rate:.2%}")

    results.extend(model_results)

    # Store the results in a JSON file after each model is tested
    with open(output_json, mode="w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    # Append the results to the Markdown file
    with open(output_md, mode="a", encoding="utf-8") as file:
        for result in model_results:
            file.write(f"| {result['Model']} | {result['Prompt']} | {result['Jailbroken']} |\n")

# Create a chart to show the jailbroken rates
jailbroken_rates = []

for jailbreak_model in model_names:
    jailbroken_count = sum(1 for result in results if result["Model"] == jailbreak_model and result["Jailbroken"])
    total_count = sum(1 for result in results if result["Model"] == jailbreak_model)
    jailbroken_rate = jailbroken_count / total_count if total_count > 0 else 0
    jailbroken_rates.append(jailbroken_rate)

plt.figure(figsize=(10, 6))
plt.bar(model_names, jailbroken_rates, color='skyblue')
plt.xlabel('Model')
plt.ylabel('Jailbroken Rate')
plt.title('Jailbroken Rate by Model')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('jailbroken_rates_chart.png')
plt.show()

print(f"Results stored in {output_json} and {output_md}")
