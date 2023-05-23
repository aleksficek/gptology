import os
import json
import openai
import request


def get_python_files(path, allowlist, blocklist):
    python_files = []
    for root, dirs, files in os.walk(path):
        for blocked in blocklist:
            if blocked in dirs:
                dirs.remove(blocked)
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

# Step 3: Parse and preprocess your Python files
def read_files(python_files):
    file_contents = []
    for file in python_files:
        with open(file, 'r') as f:
            file_contents.append(f.read())
    return file_contents

def format_prompt(python_files, file_contents, input):
    prompt = "Please make : "
    final_input = f"{prompt}{input}"

repository_path = "/Users/aficek/software/gptology"
allowlist = ["flask-server", "client", "src"]
blocklist = ["myenv", "auto", ".vscode"]
python_files = get_python_files(repository_path, allowlist, blocklist)
file_contents = read_files(python_files)

print("Done scraping")



text_input = "test"
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=text_input,
    temperature=0.5,
    max_tokens=256,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )


print(response['choices'][0]['text'])

