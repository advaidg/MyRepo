import requests
import json

# Replace these with your ServiceNow instance details and credentials
instance_url = 'https://your-instance.service-now.com'
username = 'your-username'
password = 'your-password'

# API endpoint for creating Requested Items
create_ritm_endpoint = '/api/now/table/sc_req_item'

# JSON data for the Requested Item
ritm_data = {
    "short_description": "Python Test RITM",
    "description": "This is a test RITM created via Python script.",
    "cat_item": "your_catalog_item_id",
    "requested_for": "your_user_id",
    "state": 1,  # "1" represents "Draft" state
    "variables": {
        "variable_name": "variable_value",
        # Add more variables and their values as needed
    }
}

# Set up the request headers
headers = {
    'Content-Type': 'application/json',
}

# Encode your credentials for basic authentication
auth = (username, password)

# Make the POST request to create the Requested Item
response = requests.post(
    f'{instance_url}{create_ritm_endpoint}',
    data=json.dumps(ritm_data),
    headers=headers,
    auth=auth
)

if response.status_code == 201:
    print('Requested Item created successfully.')
    ritm_data = response.json()
    ritm_number = ritm_data.get('result', {}).get('number')
    print(f'Requested Item Number: {ritm_number}')
else:
    print(f'Failed to create the Requested Item. Status Code: {response.status_code}')
    print(response.text)
