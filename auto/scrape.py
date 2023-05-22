import os

def get_python_files(path):
    python_files = []
    for root, dirs, files in os.walk(path):
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

repository_path = "/Users/aficek/software/gptology"
python_files = get_python_files(repository_path)
file_contents = read_files(python_files)

print("Done scraping")

