import os
import json
import openai
import requests
import re


def get_python_files(path, allowlist=[], blocklist=[]):
    python_files = []
    for root, dirs, files in os.walk(path):
        for blocked in blocklist:
            if blocked in dirs:
                dirs.remove(blocked)
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def read_files(python_files):
    file_contents = []
    for file in python_files:
        with open(file, 'r') as f:
            file_contents.append(f.read())
    return file_contents

def format_prompt(python_files, file_contents, prompt):
    input = {}
    for i, file in enumerate(python_files):
        input[file] = file_contents[i]
    final_input = f"{prompt}{input}"
    return final_input

def write_openai_choice(response_choice, directory_path):
    files = os.listdir(directory_path)
    pattern = re.compile(r'output_(\d+)\.txt')
    numbers = [int(pattern.match(f).group(1)) for f in files if pattern.match(f)]
    if not numbers:
        max_num = 0
    else:
        max_num = max(numbers)
    new_filename = os.path.join(directory_path, f"output_{max_num + 1}.txt")
    with open(new_filename, 'w') as f:
        f.write(response_choice)


def call_openai(text_input, mock=True, mocked_output=None):
    if mock is True:
        with open(mocked_output, "r") as f:
            response = {"choices": [{"message": { "content": f.read()}}]}
    else:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": text_input}],
            temperature=0.5,
        )
        print("Open AI Response: ", response)
        for i in response['choices']:
            write_openai_choice(i['message']['content'], "/Users/aficek/software/gptology/openai_outputs")

    return response['choices'][0]['message']['content']

def write_file(original_file, write_output, target_file, prompt):
    # output = write_output[len(prompt):]
    
    start_index = write_output.find(original_file[0][:15])
    end_index = write_output.find(original_file[0][len(original_file)-15:]) + len(original_file[0][len(original_file)-15:])
    if start_index == -1 or end_index == -1:
        ValueError("Could not find start or end")
    output = write_output[start_index:end_index]

    with open(target_file, 'w') as f:
        f.write(output)
    print("Writen to file: ", target_file)


repository_path = "/Users/aficek/software/gptology/evolve_client"
allowlist = ["flask-server", "client", "src"]
blocklist = ["myenv", "auto", ".vscode"]
# python_files = get_python_files(repository_path, allowlist, blocklist)
python_files = ["/Users/aficek/software/gptology/evolve_client/simple.py"]
print(python_files)

file_contents = read_files(python_files)
print(file_contents)

prompt = "Here is the code for a python file I am working on. Please add a simple feature to it and return me the code for the file. The code should compile and run in its entirety. Please include all of the code a <start> and an <end> tokens: "
input_text = format_prompt(python_files, file_contents, prompt)

response = call_openai(input_text, True, "/Users/aficek/software/gptology/openai_outputs/output_2.txt")
# response = call_openai(input_text, False)
print(response)


write_file(file_contents, response, repository_path + "/simple_test.py", prompt)
