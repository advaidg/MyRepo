import requests

ritm_number = "RITM1234567"

# ServiceNow REST API endpoints for RITM, status, and comments
ritm_url = f"https://{instance}.service-now.com/api/now/table/sc_req_item/{ritm_number}"
status_url = f"https://{instance}.service-now.com/api/now/table/task?sysparm_query=request_item={ritm_number}&sysparm_display_value=true"
comments_url = f"https://{instance}.service-now.com/api/now/table/sys_journal_field?sysparm_query=element_id={ritm_number}&sysparm_display_value=true"

# Set up authentication
auth = (username, password)

# Define the headers
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

try:
    # Make the GET request to fetch RITM details
    response_ritm = requests.get(ritm_url, auth=auth, headers=headers)
    response_status = requests.get(status_url, auth=auth, headers=headers)
    response_comments = requests.get(comments_url, auth=auth, headers=headers)

    # Check if the requests were successful (HTTP status code 200)
    if response_ritm.status_code == 200:
        ritm_data = response_ritm.json()["result"]
        
        # Now you can access specific fields in the RITM data
        short_description = ritm_data.get("short_description")
        description = ritm_data.get("description")
        assigned_to = ritm_data.get("assigned_to")
        
        # Print or use the retrieved data as needed
        print(f"RITM Number: {ritm_number}")
        print(f"Short Description: {short_description}")
        print(f"Description: {description}")
        print(f"Assigned To: {assigned_to}")

    if response_status.status_code == 200:
        status_data = response_status.json()["result"]
        if status_data:
            current_status = status_data[0].get("state")
            print(f"Current Status: {current_status}")

    if response_comments.status_code == 200:
        comments_data = response_comments.json()["result"]
        if comments_data:
            comments = [entry.get("value") for entry in comments_data]
            print("Comments:")
            for comment in comments:
                print(comment)
    else:
        print(f"Failed to retrieve data. HTTP Status Code: {response_status.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Request Exception: {e}")
except Exception as ex:
    print(f"An error occurred: {ex}")
