app = Flask(__name__)

# Define the ServiceNow API endpoint URL and API key
SERVICE_NOW_API_URL = "https://your-instance-name.service-now.com/api/now/table/incident"
API_KEY = "your-api-key"

@app.route('/get_incidents', methods=['GET'])
def get_incidents():
    # Define headers with the API key
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }

    try:
        # Make a GET request to the ServiceNow API
        response = requests.get(SERVICE_NOW_API_URL, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({'error': 'Failed to retrieve incidents from ServiceNow'}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to connect to ServiceNow API'}), 500

if __name__ == '__main__':
    app.run(debug=True)
