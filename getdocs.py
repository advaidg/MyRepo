import requests

# ServiceNow instance URL
instance_url = "https://your-instance.service-now.com"

# ServiceNow credentials
username = "your-username"
password = "your-password"

# Search query
query = "Your search query here"

# API endpoint for the Knowledge Base
api_endpoint = "/api/now/table/kb_knowledge"

# Construct the API request URL
url = f"{instance_url}{api_endpoint}"

# Parameters for the request
params = {
    "sysparm_query": f"short_descriptionLIKE{query}",
    "sysparm_limit": 3,
}

# Make the API request
response = requests.get(url, auth=(username, password), params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Extract and print the links to the first 3 results
    for record in data.get("result", []):
        link = record.get("sys_id")  # Adjust this to match your KB record URL structure
        print(f"Title: {record.get('short_description')}")
        print(f"Link: {instance_url}/kb_view.do?sysparm_article={link}")
else:
    print(f"Error: {response.status_code} - {response.text}")
