from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Directory containing the Python scripts
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name):
    script_path = os.path.join(SCRIPT_DIR, script_name)
    result = subprocess.run(['python', script_path])
    if result.returncode != 0:
        return jsonify({"output": f"An error occurred: {result.stderr}"}), 500
    return jsonify({"output": result.stdout})

def write_array_to_file(data, filename):
    with open(filename, 'w') as file:
        for row in data['payload']:
            # Convert each row to a space-separated string and write to the file
            file.write(' '.join(map(str, row)) + '\n')


@app.route('/run-bruteforce', methods=['POST'])
def run_bruteforce():
    data = request.get_json()
    write_array_to_file(data, 'input.txt')
    return run_script('bruteforce.py')

@app.route('/run-divide', methods=['POST'])
def run_divide():
    data = request.get_json()
    write_array_to_file(data, 'input.txt')
    return run_script('divide.py')

@app.route('/run-gramham', methods=['POST'])
def run_gramham():
    data = request.get_json()
    print(data)
    write_array_to_file(data, 'input.txt')
    return run_script('Gramham.py')

@app.route('/run-jarvis', methods=['POST'])
def run_jarvis():
    data = request.get_json()
    write_array_to_file(data, 'input.txt')
    return run_script('jarvis.py')

@app.route('/run-monotone', methods=['POST'])
def run_monotone():
    data = request.get_json()
    write_array_to_file(data, 'input.txt')
    return run_script('monotone.py')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
