import requests

# URL for the Flask API
url = 'http://127.0.0.1:5000/users'

# Data to send in the POST request (example user details)
data = {
    "name": "John Doe",
    "email": "johndoe@example.com"
}

# Send the POST request to create a new user
response = requests.post(url, json=data)

# Check if the response status code is 201 (Created)
if response.status_code == 201:
    print("User created successfully:", response.json())
else:
    print("Failed to create user:", response.json())
