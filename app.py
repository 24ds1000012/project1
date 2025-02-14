from flask import Flask, jsonify, request
import os
import subprocess
import json
import requests

app = Flask(__name__)

#PORT
PORT = 8000
@app.route('/run', methods=['POST'])
def run_task():
    task_description = request.args.get('task')

    try:
        # Parse the task description and determine which task to run
        if "install uv and run" in task_description:
            email = task_description.split("${user.email}")[1].strip()
            install_uv_and_run_script(email)
        elif "format" in task_description:
            file_path = task_description.split(" ")[1]  # assuming file path is provided
            format_file_with_prettier(file_path)
        # Add more conditions for other tasks as needed
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

@app.route('/read', methods=['GET'])
def read_file():
    path = request.args.get('path')
    
    if not is_safe_path(path):
        return jsonify({"status": "error", "message": "Invalid file path"}), 400
    
    try:
        with open(path, 'r') as file:
            return file.read(), 200
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "File not found"}), 404
    
def is_safe_path(path):
    return path.startswith("/data/")

#3.1 Task A1: Install uv and Run the Python Script
def install_uv_and_run_script(email):
    subprocess.run(["pip", "install", "uv"], check=True)
    subprocess.run(["python", "datagen.py", email], check=True)

#3.2 Task A2: Format with Prettier
def format_file_with_prettier(file_path):
    subprocess.run(["npm", "install", "prettier@3.4.2"], check=True)
    subprocess.run(["npx", "prettier", "--write", file_path], check=True)

#3.3 Task A3: Count Wednesdays in a List of Dates
from datetime import datetime

def count_wednesdays(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    wednesdays_count = sum(1 for line in lines if datetime.strptime(line.strip(), '%Y-%m-%d').weekday() == 2)
    
    with open(output_file, 'w') as file:
        file.write(str(wednesdays_count))

def extract_email_with_llm(email_content):
    api_url = "https://api.llm.example.com"
    headers = {
        "Authorization": f"Bearer {os.environ['AIPROXY_TOKEN']}",
    }
    payload = {
        "input": email_content,
        "task": "extract_sender_email"
    }
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()['sender_email']

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)



