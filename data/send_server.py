import requests
import json

def post_data_to_api(url, headers, payload):
    try:
        if not isinstance(payload, str):
            payload = json.dumps(payload)

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            print("POST request successful.")
            print("Response:")
            print(response.text)
        else:
            print(f"POST request failed. Status code: {response.status_code}")
            print("Response:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage:
url = "http://127.0.0.1:8000/v1/api/admin/category/"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your_access_token_here',
    'Cookie': 'token=your_cookie_token_here'
}
payload = {
    "name": "New Category",
    "description": "This is a new category"
}

# post_data_to_api(url, headers, payload)
with open("Category_data.json", 'r') as f:
    data = json.load(f)
print(len(data))
for item in data:
    url = "http://127.0.0.1:8000/v1/api/admin/category/"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IlRlc3RpbmczQGdtYWlsLmNvbSIsImlhdCI6MTcxODgyNjAzOSwibmJmIjoxNzE4ODI1NzM5LCJleHAiOjE3MTk0MzA4Mzl9.7NeDRdIjJEDDXmLoFL917QqqLwp2UhEBN0dXZbZLdUI',
        'Cookie': 'token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IlRlc3RpbmczQGdtYWlsLmNvbSIsImlhdCI6MTcxODgyNjAzOSwibmJmIjoxNzE4ODI1NzM5LCJleHAiOjE3MTk0MzA4Mzl9.7NeDRdIjJEDDXmLoFL917QqqLwp2UhEBN0dXZbZLdUI'
    }
    
    post_data_to_api(url, headers, item)

    