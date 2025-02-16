import subprocess
import datetime
import json
import os
import re
import pytesseract
from PIL import Image
import sqlite3
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
import openai
import numpy as np

# Use AIPROXY_TOKEN environment variable for API key
openai.api_key = os.environ.get("AIPROXY_TOKEN")

def handle_task_A1(task_description):
    email = extract_email_from_task(task_description)
    if not email:
        return "No email provided"
    
    try:
        subprocess.run(['pip', 'install', 'uv'], check=True)
    except subprocess.CalledProcessError:
        return "Failed to install uv"
    
    try:
        subprocess.run(['python3', 'datagen.py', email], check=True)
        return f"Data generated for {email}"
    except subprocess.CalledProcessError:
        return "Failed to run datagen.py"

def handle_task_A2():
    try:
        subprocess.run(['npx', 'prettier', '--write', '/data/format.md'], check=True)
        return "Formatted /data/format.md successfully"
    except subprocess.CalledProcessError:
        return "Failed to format file"

def handle_task_A3():
    try:
        with open('/data/dates.txt', 'r') as file:
            dates = file.readlines()

        wednesday_count = sum(1 for date_str in dates if datetime.datetime.strptime(date_str.strip(), '%Y-%m-%d').weekday() == 2)

        with open('/data/dates-wednesdays.txt', 'w') as file:
            file.write(str(wednesday_count))

        return f"Found {wednesday_count} Wednesdays"
    except Exception as e:
        return f"Error counting Wednesdays: {str(e)}"

def handle_task_A4():
    try:
        with open('/data/contacts.json', 'r') as file:
            contacts = json.load(file)

        contacts.sort(key=lambda x: (x['last_name'], x['first_name']))

        with open('/data/contacts-sorted.json', 'w') as file:
            json.dump(contacts, file, indent=4)

        return "Contacts sorted successfully"
    except Exception as e:
        return f"Error sorting contacts: {str(e)}"

def handle_task_A5():
    try:
        log_files = sorted([f for f in os.listdir('/data/logs/') if f.endswith('.log')],
                           key=lambda x: os.path.getmtime(f'/data/logs/{x}'), reverse=True)[:10]

        recent_lines = []
        for log_file in log_files:
            with open(f'/data/logs/{log_file}', 'r') as file:
                recent_lines.append(file.readline().strip())

        with open('/data/logs-recent.txt', 'w') as file:
            file.write("\n".join(recent_lines))

        return "First line of 10 recent log files written"
    except Exception as e:
        return f"Error extracting log lines: {str(e)}"

def handle_task_A6():
    try:
        md_files = [f for f in os.listdir('/data/docs/') if f.endswith('.md')]
        index = {}

        for md_file in md_files:
            with open(f'/data/docs/{md_file}', 'r') as file:
                for line in file:
                    if line.startswith('# '):
                        index[md_file] = line.strip('# ').strip()
                        break

        with open('/data/docs/index.json', 'w') as file:
            json.dump(index, file, indent=4)

        return "Created index.json with H1 headers"
    except Exception as e:
        return f"Error extracting H1 headers: {str(e)}"

def handle_task_A7():
    try:
        with open('/data/email.txt', 'r') as file:
            email_content = file.read()

        sender_email = re.search(r'\S+@\S+', email_content)
        if sender_email:
            with open('/data/email-sender.txt', 'w') as file:
                file.write(sender_email.group(0))

            return "Extracted email and saved to /data/email-sender.txt"
        else:
            return "No email found in content"
    except Exception as e:
        return f"Error extracting email: {str(e)}"

def handle_task_A8():
    try:
        image = Image.open('/data/credit-card.png')
        text = pytesseract.image_to_string(image)
        
        cc_number = re.sub(r'\D', '', text)

        with open('/data/credit-card.txt', 'w') as file:
            file.write(cc_number)

        return "Extracted credit card number and saved to /data/credit-card.txt"
    except Exception as e:
        return f"Error extracting credit card number: {str(e)}"

def handle_task_A9():
    try:
        with open('/data/comments.txt', 'r') as file:
            comments = file.readlines()

        similar_pair = find_most_similar_comments(comments)

        with open('/data/comments-similar.txt', 'w') as file:
            file.write("\n".join(similar_pair))

        return "Found and saved most similar comments"
    except Exception as e:
        return f"Error processing comments: {str(e)}"

def find_most_similar_comments(comments):
    embeddings = []
    for comment in comments:
        response = openai.Embedding.create(input=comment, model="text-embedding-ada-002")
        embeddings.append(response['data'][0]['embedding'])
    
    max_similarity = -1
    most_similar_pair = (None, None)
    
    for i in range(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            if sim > max_similarity:
                max_similarity = sim
                most_similar_pair = (comments[i], comments[j])

    return most_similar_pair

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_description = request.form.get('task_description')
        # Process the task description here
        return f"Task Description Received: {task_description}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
