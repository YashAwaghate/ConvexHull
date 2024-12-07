from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import base64
from io import BytesIO
from matplotlib.figure import Figure

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
    # write_array_to_file(data, 'input.txt')
    run_script('bruteforce.py')
    with open('/tmp/output.gif', 'rb') as gif_file:
        buf = gif_file.read()
    print("Image Data")
    image_data = base64.b64encode(buf).decode("ascii")    
    return f"data:image/png;base64,{image_data}"

# @app.route('/run-divide', methods=['POST'])
# def run_divide():
#     data = request.get_json()
#     write_array_to_file(data, 'input.txt')
#     return run_script('divide.py')
@app.route('/run-divide', methods=['POST'])
def run_divide():
    # Log raw request data for debugging
    raw_data = request.get_data(as_text=True)
    print(f"Raw received data: {raw_data}")  # Log raw input

    try:
        # Parse the request as JSON
        json_data = request.get_json()
        print(f"Parsed JSON data: {json_data}")  # Log parsed JSON
        write_array_to_file(json_data, 'input.txt')
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return jsonify({"error": "Invalid input format"}), 400

    run_script('divide.py')
    with open('output.gif', 'rb') as gif_file:
        buf = gif_file.read()
    image_data = base64.b64encode(buf).decode("ascii")
    return f"data:image/png;base64,{image_data}"



@app.route('/run-gramham', methods=['POST'])
def run_gramham():
    data = request.get_json()
    print(data)
    write_array_to_file(data, 'input.txt')
    run_script('Gramham.py')
    with open('output.gif', 'rb') as gif_file:
        buf = gif_file.read()
    image_data = base64.b64encode(buf).decode("ascii")
    return f"data:image/png;base64,{image_data}"

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
