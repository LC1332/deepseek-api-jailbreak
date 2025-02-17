import csv
import random

class PromptSelector:
    def __init__(self, csv_filename, column):
        self.csv_filename = csv_filename
        self.column = column
        self.prompts = self._load_prompts()
        self.used_prompts = set()

    def _load_prompts(self):
        try:
            with open(self.csv_filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                return [row[self.column] for row in reader if self.column in row and row[self.column]]
        except FileNotFoundError:
            print(f"Error: The file '{self.csv_filename}' was not found.")
        except KeyError:
            print(f"Error: The CSV file does not contain a '{self.column}' column.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return []

    def get_next_prompt(self):
        available_prompts = list(set(self.prompts) - self.used_prompts)
        if not available_prompts:
            print("All prompts have been used. Resetting...")
            self.used_prompts.clear()
            available_prompts = self.prompts[:]
        
        if available_prompts:
            prompt = random.choice(available_prompts)
            self.used_prompts.add(prompt)
            return prompt
        return None

'''example usage
if __name__ == "__main__":
    csv_filename = "harmful_behaviors_jailbreakbench.csv"  
    column_name = "Goal"  
    selector = PromptSelector(csv_filename, column_name)
    for i in range(10):
        prompt = selector.get_next_prompt()
        
        if prompt:
            print("Next prompt:", prompt)
'''