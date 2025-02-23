import os

# Path to the markdown file
md_path = "/home/christianwang/deepseek-api-jailbreak/wzq_exp/jailbroken_results.md"

# Read all lines from the markdown file
with open(md_path, mode="r", encoding="utf-8") as file:
    lines = file.readlines()

# Define the row ranges (0-indexed) and the corresponding model to insert:
# Region definitions:
# Region 1: rows 5 to 64     => indices [4, 64)
# Region 2: rows 65 to 124   => indices [64, 124)
# Region 3: rows 125 to 184  => indices [124, 184)
# Region 4: rows 185 to 244  => indices [184, 244)
ranges = [
    (4, 34, "阿里云DeepSeek-R1"),
    (34, 64, "阿里云DeepSeek-V3"),
]

modified_lines = []
for i, line in enumerate(lines):
    # Process only table rows (starting with "|" marker)
    if line.startswith("|"):
        # Check each defined range
        for start_index, end_index, model_to_add in ranges:
            if start_index <= i < end_index:
                parts = line.split("|")
                # parts[0] is empty because the line starts with a pipe.
                # If the first cell (index 1) isn't already equal to our model, then insert it.
                if parts[1].strip() != model_to_add:
                    parts.insert(1, model_to_add)
                    new_line = "|".join(parts)
                    # Ensure the line starts with "|" and ends with "|\n"
                    if not new_line.startswith("|"):
                        new_line = "|" + new_line
                    if not new_line.rstrip().endswith("|"):
                        new_line = new_line.rstrip() + "|\n"
                    line = new_line
                break  # Once processed, break out of range loop
    modified_lines.append(line)

# Write modified content back to file
with open(md_path, mode="w", encoding="utf-8") as file:
    file.writelines(modified_lines)

print(f"Updated regions in {md_path}:")
for start, end, model in ranges:
    print(f"Region {model}: rows {start + 1} to {end}")
