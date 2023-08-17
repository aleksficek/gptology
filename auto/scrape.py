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

def get_next_filename(base_dir):
    """
    Determines the next filename based on existing files in the base_dir.
    Returns the next filename as a string.
    """
    existing_files = os.listdir(base_dir)
    output_files = [f for f in existing_files if f.startswith('output_') and f.endswith('.txt')]
    
    # Extract the num values from the existing files and find the max
    nums = [int(f.split('_')[1].split('.')[0]) for f in output_files]
    next_num = max(nums) + 1 if nums else 1

    return next_num

def backup_openai_response(response, base_dir):
    """
    Writes to the next output_{num}_{num2}.txt based on existing files in base_dir.
    Writes each element of input_list to the next largest num2 for the given num.
    """
    next_num = get_next_filename(base_dir)
    next_num2 = 0

    for data in response["choices"]:
        filename = os.path.join(base_dir, f'output_{next_num}_{next_num2}.txt')
        with open(filename, 'w') as f:
            f.write(data["message"]["content"])
        next_num2 += 1


# def write_openai_choices(response_choice, directory_path):
#     files = os.listdir(directory_path)
#     pattern = re.compile(r'output_(\d+)\.txt')
#     numbers = [int(pattern.match(f).group(1)) for f in files if pattern.match(f)]
#     if not numbers:
#         max_num = 0
#     else:
#         max_num = max(numbers)
#     base_filename = os.path.join(directory_path, f"output_{max_num + 1}")


#     max_num_2

#     for each_choice in range(len(response_choice["choices"])):

#         new_filename = f'{base_filename}_{max_num_2}.txt'
#         with open(base_filename, 'w') as f:
#             f.write(each_choice)


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
        backup_openai_response(response, "/Users/aficek/software/gptology/openai_outputs")

    return response

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

user_input = "something"
while user_input != "":
    user_input = input(f"Which option would you like to view, select from 0 to {len(response['choices'])}: ")
    write_file(file_contents, response["choices"][int(user_input)]["message"]["content"], repository_path + "/simple_test.py", prompt)


# response['choices'][0]['message']['content']
# response = call_openai(input_text, False)
# print(response)

# write_file(file_contents, response, repository_path + "/simple_test.py", prompt)

