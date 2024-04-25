import subprocess
import json

def create_requirements():
    # Run pip freeze and capture the output
    result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE)

    # Decode the result to a string
    pip_freeze_output = result.stdout.decode('utf-8')

    # Split the output into lines
    packages = pip_freeze_output.splitlines()

    # Prepare the new requirements content
    new_requirements = [pkg.replace('==', '<=') for pkg in packages]

    # Write the modified requirements to a file
    with open('requirements_less_than.txt', 'w') as f:
        for line in new_requirements:
            f.write(line + '\n')

    print('requirements_less_than.txt generated successfully.')


def read_json(file_path):# Open the file in read mode
    with open(file_path, 'r') as file:
        # Load its content and convert it into a dictionary
        data = json.load(file)
        return data

