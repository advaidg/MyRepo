from flask import Flask, request, jsonify
import cx_Oracle

app = Flask(__name__)

# Oracle database connection configuration
dsn_tns = cx_Oracle.makedsn('your_host', 'your_port', service_name='your_service_name')
connection = cx_Oracle.connect(user='your_username', password='your_password', dsn=dsn_tns)

@app.route('/get_data', methods=['POST'])
def get_data():
    # Get fl_id and fn_code from the frontend
    fl_id = request.json.get('fl_id')
    fn_code = request.json.get('fn_code')

    # Query to fetch data from the Oracle database
    query = f"""
    SELECT col1, col2, col3, start_time, end_time,
    (end_time - start_time) AS elapsed_time
    FROM your_table
    WHERE fl_id = :fl_id AND fn_code = :fn_code
    """

    cursor = connection.cursor()
    cursor.execute(query, [fl_id, fn_code])
    rows = cursor.fetchall()

    # Convert data to JSON format
    result = []
    for row in rows:
        result.append({
            'col1': row[0],
            'col2': row[1],
            'col3': row[2],
            'start_time': row[3],
            'end_time': row[4],
            'elapsed_time': row[5]
        })

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
