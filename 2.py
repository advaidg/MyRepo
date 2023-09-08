import requests
from requests.auth import HTTPBasicAuth  # Import HTTPBasicAuth for basic authentication

# Set your SonarQube instance URL, username, and password
SONARQUBE_URL = "https://your-sonarqube-url.com"
USERNAME = "your-username"
PASSWORD = "your-password"

def fetch_projects_with_quality_gate_status():
    projects_with_status = {}
    
    for status in QUALITY_GATE_STATUSES:
        response = requests.get(
            f"{SONARQUBE_URL}/api/qualitygates/search",
            auth=HTTPBasicAuth(USERNAME, PASSWORD),  # Use basic authentication
        )
        response.raise_for_status()
        data = response.json()
        gate_id = [gate["id"] for gate in data["qualitygates"] if gate["name"] == status][0]
        
        response = requests.get(
            f"{SONARQUBE_URL}/api/projects/search",
            params={"gateId": gate_id},
            auth=HTTPBasicAuth(USERNAME, PASSWORD),  # Use basic authentication
        )
        response.raise_for_status()
        projects_with_status[status] = len(response.json()["components"])
    
    return projects_with_status

if __name__ == "__main__":
    QUALITY_GATE_STATUSES = ["E", "F"]  # Define the quality gate statuses you want to count
    projects_with_status = fetch_projects_with_quality_gate_status()
    
    print("Number of applications with quality gate status:")
    for status, count in projects_with_status.items():
        print(f"{status}: {count}")
