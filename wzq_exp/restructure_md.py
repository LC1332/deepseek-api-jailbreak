import re

def restructure_markdown(input_file, output_file):
    """
    Restructures a markdown table to have prompts as the first column
    and models as subsequent columns with jailbreak status,
    using tick and cross emojis.
    """

    data = {}
    models = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skip header lines
    data_lines = lines[3:]

    for line in data_lines:
        line = line.strip()
        if not line or not line.startswith('|'):
            continue

        parts = [p.strip() for p in re.split(r'\|', line)[1:-1]]  # Split and remove leading/trailing pipes
        if len(parts) != 3:
            continue

        model, prompt, judgment = parts
        models.add(model)

        if prompt not in data:
            data[prompt] = {}
        data[prompt][model] = judgment.lower() == 'true'

    models = sorted(list(models))
    prompts = sorted(list(data.keys()))

    # Write the restructured data to a new markdown file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("# Restructured Results\n\n")

        # Create header row
        header = ["Prompt"] + models
        outfile.write("| " + " | ".join(header) + " |\n")
        outfile.write("|" + "---|" * len(header) + "\n")

        # Write data rows
        for prompt in prompts:
            row = [prompt]
            for model in models:
                jailbroken = data[prompt].get(model, False)
                row.append("✔️" if jailbroken else "❌")  # Use tick and cross emojis
            outfile.write("| " + " | ".join(row) + " |\n")

    print(f"Restructured data written to {output_file}")


if __name__ == "__main__":
    input_file = "/home/christianwang/deepseek-api-jailbreak/jailbreak_result/jailbroken_results3.md"
    output_file = "/home/christianwang/deepseek-api-jailbreak/wzq_exp/restructured_results.md"  # Output in your wzq_exp directory
    restructure_markdown(input_file, output_file)