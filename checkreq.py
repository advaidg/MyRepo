import requests
import json

# ServiceNow instance URL
instance_url = "https://your-instance.service-now.com"

# Replace 'your_username' and 'your_password' with your ServiceNow credentials
username = 'your_username'
password = 'your_password'

# Replace 'REQ001' with the actual REQ number
req_number = 'REQ001'

# Authenticate with ServiceNow and obtain an authentication token
auth_url = f"{instance_url}/api/now/v1/oauth/token"
auth_payload = {
    'grant_type': 'password',
    'client_id': 'client_id',
    'client_secret': 'client_secret',
    'username': username,
    'password': password
}

auth_response = requests.post(auth_url, data=auth_payload)
auth_data = auth_response.json()
access_token = auth_data['access_token']

# Retrieve the RITM by REQ number
ritm_url = f"{instance_url}/api/now/v1/table/rm_request"
ritm_params = {
    'sysparm_query': f'number={req_number}'
}
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

ritm_response = requests.get(ritm_url, params=ritm_params, headers=headers)
ritm_data = ritm_response.json()

if 'result' in ritm_data:
    ritm = ritm_data['result'][0]

    ritm_sys_id = ritm['sys_id']
    ritm_status = ritm['state']

    # Generate links to the RITM
    ritm_link = f"{instance_url}/nav_to.do?uri=%2Frm_request.do%3Fsys_id%3D{ritm_sys_id}"
    req_link = f"{instance_url}/nav_to.do?uri=%2Fsc_request.do%3Fsys_id%3D{ritm['sc_request']}"

    print(f"RITM Number: {ritm['number']}")
    print(f"RITM Status: {ritm_status}")
    print(f"Link to RITM: {ritm_link}")
    print(f"Link to REQ: {req_link}")
else:
    print(f"No RITM found for REQ number: {req_number}")

# Logout or perform any necessary cleanup if needed
