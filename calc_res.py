import json

with open('火山benchmark.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Filter entries that contain the "Jailbroken" key
jailbroken_entries = [entry for entry in data if "Jailbroken" in entry]

# Count entries where "Jailbroken" is True
true_count = sum(1 for entry in jailbroken_entries if entry.get("Jailbroken") is True)

total_count = len(jailbroken_entries)
proportion = true_count / total_count if total_count > 0 else 0

print("Total 'Jailbroken' entries:", total_count)
print("Number of 'Jailbroken': true occurrences:", true_count)
print("Proportion of true 'Jailbroken':", proportion)
