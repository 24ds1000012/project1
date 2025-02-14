import requests

url = "http://127.0.0.1:8000/run"
data = {
    "task": "Install uv and run datagen.py with email=24ds1000012@ds.study.iitm.ac.in"
}

# Send POST request with JSON data
response = requests.post(url, json=data)

# Print the response
print(response.status_code)  # Should be 200 if successful
print(response.json())  # Should print the response from Flask
