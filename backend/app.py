from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import base64
from io import BytesIO
from matplotlib.figure import Figure
from bruteforce import brute_main
from divide import divide_main
from Gramham import graham_main
from jarvis import jarvis_main
from monotone import monotone_main

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
        if isinstance(data, dict) and 'payload' in data:
            # JSON Input
            for row in data['payload']:
                print(row)  # Debugging
                file.write(' '.join(map(str, row)) + '\n')
        elif isinstance(data, str):
            # Plain text input: Convert to rows
            lines = data.strip().split('\n')
            for line in lines:
                print(line.strip().split())  # Debugging
                file.write(line.strip() + '\n')
        else:
            raise ValueError("Unsupported input format. Expected JSON or plain text.")

@app.route('/run-bruteforce', methods=['POST'])
def run_bruteforce():
    data = request.get_json()
    image_data = brute_main(data)
    return f"data:image/png;base64,{image_data}"


@app.route('/run-divide', methods=['POST'])
def run_divide():
    data = request.get_data()
    image_data = divide_main(data)
    return f"data:image/png;base64,{image_data}"



@app.route('/run-gramham', methods=['POST'])
def run_gramham():
    data = request.get_json()
    image_data = graham_main(data)
    return f"data:image/png;base64,{image_data}"

@app.route('/run-jarvis', methods=['POST'])
def run_jarvis():
    data = request.get_json()
    image_data = jarvis_main(data)
    return f"data:image/png;base64,{image_data}"

@app.route('/run-monotone', methods=['POST'])
def run_monotone():
    data = request.get_json()
    image_data = monotone_main(data)
    return f"data:image/png;base64,{image_data}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
