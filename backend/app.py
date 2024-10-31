from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Directory containing the Python scripts
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name):
    script_path = os.path.join(SCRIPT_DIR, script_name)
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    if result.returncode != 0:
        return jsonify({"output": f"An error occurred: {result.stderr}"}), 500
    return jsonify({"output": result.stdout})

@app.route('/run-bruteforce', methods=['GET'])
def run_bruteforce():
    return run_script('bruteforce.py')

@app.route('/run-divide', methods=['GET'])
def run_divide():
    return run_script('divide.py')

@app.route('/run-gramham', methods=['GET'])
def run_gramham():
    return run_script('Gramham.py')

@app.route('/run-jarvis', methods=['GET'])
def run_jarvis():
    return run_script('jarvis.py')

@app.route('/run-monotone', methods=['GET'])
def run_monotone():
    return run_script('monotone.py')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
